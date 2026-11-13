"""Repositórios: a única camada que conversa com o banco de dados.

A regra é: serviço não sabe SQL, rota não sabe banco. Quem precisa de dados 
pede a um repositório.
"""

from app.repositories.base import RepositorioBase
from app.repositories.tarefa import FiltroDeTarefas, TarefaRepositorio
from app.repositories.usuario import UsuarioRepositorio

__all__ = [
    "FiltroDeTarefas",
    "RepositorioBase",
    "TarefaRepositorio",
    "UsuarioRepositorio",
]