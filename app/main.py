"""Ponto de entrada: cria o app, registra as rotas e traduz erros em HTTP."""
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.api.routers import usuarios
from app.core.exceptions import (
    EmailJaCadastrado,
    ErroDeDominio,
    RecursoNaoEncontrado,
    RegraDeNegocioViolada,
)
from app.db.database import criar_tabelas

# Cada família de erro de domínio corresponde a um código HTTP. A ordem
# importa: vale o primeiro tipo que casar, do mais específico ao mais geral.
STATUS_POR_ERRO: tuple[tuple[type[ErroDeDominio], int], ...] = (
    (RecursoNaoEncontrado, 404),
    (EmailJaCadastrado, 409),
    (RegraDeNegocioViolada, 422),
    (ErroDeDominio, 400),
)


@asynccontextmanager
async def ciclo_de_vida(app: FastAPI) -> AsyncIterator[None]:
    """Prepara o banco na subida da aplicação: cria as tabelas que faltam."""
    criar_tabelas()
    yield


app = FastAPI(
    title="Todo List API",
    description="Backend do ToDo List - curso Desenvolvedor Full Stack (SENAC).",
    version="0.3.0",
    lifespan=ciclo_de_vida,
)


@app.exception_handler(ErroDeDominio)
async def tratar_erro_de_dominio(
    _request: Request, excecao: ErroDeDominio
) -> JSONResponse:
    """Converte qualquer erro de domínio na resposta HTTP correspondente.

    Um único tratador atende a hierarquia inteira de exceções — é polimorfismo
    aplicado ao tratamento de erro. As rotas não precisam conhecer códigos de
    status de negócio e o domínio não precisa conhecer HTTP.
    """
    codigo = next(
        (codigo for tipo, codigo in STATUS_POR_ERRO if isinstance(excecao, tipo)), 400
    )
    return JSONResponse(status_code=codigo, content={"detail": excecao.mensagem})


def _mensagem_de_validacao(erro: dict[str, Any]) -> tuple[str, str]:
    """Traduz um erro do Pydantic em (campo, mensagem em português)."""
    campo = str(erro["loc"][-1]) if erro.get("loc") else "dados"
    tipo = erro.get("type", "")
    ctx = erro.get("ctx", {})
    mensagens = {
        "missing": f"O campo '{campo}' é obrigatório.",
        "string_too_short": f"O campo '{campo}' precisa ter pelo menos {ctx.get('min_length')} caractere(s).",
        "string_too_long": f"O campo '{campo}' pode ter no máximo {ctx.get('max_length')} caracteres.",
        "enum": f"Valor inválido para '{campo}'. Valores aceitos: {', '.join(str(v) for v in ctx.get('expected', []))}.",
        "date_parsing": f"Data inválida em '{campo}'. Use o formato AAAA-MM-DD.",
        "date_from_datetime_parsing": f"Data inválida em '{campo}'. Use o formato AAAA-MM-DD.",
        "int_parsing": f"O campo '{campo}' precisa ser um número inteiro.",
        "greater_than": f"O campo '{campo}' precisa ser no mínimo {ctx.get('gt')}.",
        "less_than_equal": f"O campo '{campo}' pode ser no máximo {ctx.get('le')}.",
        "json_invalid": "O corpo da requisição não é um JSON válido.",
    }
    if tipo == "value_error":
        if campo == "email":
            return campo, "E-mail inválido."
        return campo, str(erro.get("msg", "")).removeprefix("Value error, ")
    return campo, mensagens.get(tipo, f"Valor inválido em '{campo}'.")


@app.exception_handler(RequestValidationError)
async def tratar_erro_de_validacao(
    _request: Request, excecao: RequestValidationError
) -> JSONResponse:
    """Traduz erros de validação do Pydantic em respostas HTTP 422."""
    erros = [
        {"campo": campo, "mensagem": mensagem}
        for campo, mensagem in map(_mensagem_de_validacao, excecao.errors())
    ]
    return JSONResponse(
        status_code=422,
        content={
            "detail": erros[0]["mensagem"] if erros else "Dados inválidos.",
            "erros": erros,
        },
    )


app.include_router(usuarios.router)


@app.get("/", tags=["Status"], summary="Verificar se a API está no ar")
def raiz() -> dict[str, str]:
    """Confirma que a API está no ar e indica onde está a documentação."""
    return {"mensagem": "Todo List API no ar", "documentacao": "/docs"}