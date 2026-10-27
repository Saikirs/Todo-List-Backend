"""Modelos de domínio: as entidades do sistema, com seus dados e suas regras.

Cada entidade é responsável por manter o próprio estado válido: o `Usuario`
normaliza o próprio e-mail e só aceita a senha em forma de hash.
"""

from app.models.usuario import Usuario

__all__ = [Usuario]