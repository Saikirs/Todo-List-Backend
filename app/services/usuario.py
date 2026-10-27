"""Operações de cadastro de usuários."""

from __future__ import annotations

from app.core.security import HashDeSenha
from app.models import Usuario
from app.repositories import UsuarioRepositorio


class UsuarioServico:
    """Operações de cadastro de usuários."""

    def __init__(self, repositorio: UsuarioRepositorio, hasher: HashDeSenha) -> None:
        self._repositorio = repositorio
        self._hasher = hasher

    def cadastrar(self, nome: str, email: str, senha: str) -> Usuario:
        """Cadastra um usuário com a senha em hash."""
        usuario = Usuario(nome=nome, email=email)
        usuario.definir_senha(senha, self._hasher)  # RN-05
        return self._repositorio.salvar(usuario)