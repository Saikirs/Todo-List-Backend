"""Modelos de domínio: as entidades do sistema, com seus dados e suas regras.

Cada entidade é responsável por manter o próprio estado válido: o `Usuario`
normaliza o próprio e-mail e só aceita a senha em forma de hash; a `Tarefa`
nasce sempre pendente e não deixa ninguém mudar o status de fora.
"""

# Importar as entidades aqui regista as tabelas no SQLAlchemy (é o que
# `criar_tabelas()` usa) e permite escrever `from app.models import Tarefa`.
from app.models.tarefa import Tarefa
from app.models.usuario import Usuario

__all__ = ["Tarefa", "Usuario"] 