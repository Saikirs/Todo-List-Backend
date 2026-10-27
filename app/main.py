"""Ponto de entrada: cria o app e registra as rotas."""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.routers import usuarios
from app.db.database import criar_tabelas


@asynccontextmanager
async def ciclo_de_vida(app: FastAPI) -> AsyncIterator[None]:
    """Prepara o banco na subida da aplicação: cria as tabelas que faltam."""
    criar_tabelas()
    yield


app = FastAPI(
    title="Todo List API",
    description="Backend do ToDo List — curso Desenvolvedor Full Stack (SENAC).",
    version="0.2.0",
    lifespan=ciclo_de_vida,
)

app.include_router(usuarios.router)


@app.get("/", tags=["Status"], summary="Verificar se a API está no ar")
def raiz() -> dict[str, str]:
    """Confirma que a API está funcionando e indica onde está a documentação."""
    return {"mensagem": "Todo List API no ar", "documentacao": "/docs"}