"""Serviços de aplicação: onde as operações do sistema são orquestradas.

Um serviço recebe repositórios e colaboradores pelo construtor (injeção de dependência), aplica as regras de negócio e levanta exceções de domínio. Ele não conhece HTTP: não importa `fastapi`, não devolve códigos de status. O mesmo serviço funcionaria em um programa de terminal.
"""

from app.services.usuario import UsuarioServico

__all__ = [
    "UsuarioServico",
]