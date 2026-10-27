"""Endpoints de usuário: cadastro.

A rota traduz HTTP em uma chamada de serviço e devolve o resultado. Não há
consulta ao banco, `if` de regra de negócio nem `raise HTTPException`.
"""

from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.api.dependencies import obter_usuario_servico
from app.schemas import UsuarioCreate, UsuarioOut
from app.services import UsuarioServico

router = APIRouter(prefix="/usuarios", tags=["Usuários"])


@router.post(
    "",
    response_model=UsuarioOut,
    status_code=status.HTTP_201_CREATED,
    summary="Cadastrar usuário",
)
def cadastrar_usuario(
    dados: UsuarioCreate,
    servico: Annotated[UsuarioServico, Depends(obter_usuario_servico)],
) -> UsuarioOut:
    """Cadastra um novo usuário com a senha armazenada como hash."""
    return servico.cadastrar(dados.nome, dados.email, dados.senha)