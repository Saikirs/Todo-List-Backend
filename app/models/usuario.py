"""Entidade Usuario: representa um usuário do sistema, com nome, e-mail e senha (em hash)."""
from __future__ import annotations
from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import validates
from app.core.datas import agora_utc
from app.core.exceptions import ValorInvalido
from app.core.security import HashDeSenha
from app.db.database import Base


class Usuario(Base):
    """Usuário do sistema."""
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(120), nullable=False)
    email = Column(String(180), nullable=False, unique=True, index=True)
    # O hash é privado; nenhuma camada acima precisa - nem deve - ler este
    # valor. Quem quiser conferir uma senha usa apenas senha_confere.
    _senha_hash = Column("senha_hash", String(255), nullable=False)
    criado_em = Column(DateTime(timezone=True), nullable=False, default=agora_utc)

    def __init__(self, nome: str, email: str) -> None:
        """Cria um usuário ainda sem senha definida."""
        self.nome = nome
        self.email = self.normalizar_email(email)

    @staticmethod
    def normalizar_email(email: str) -> str:
        """Normaliza o e-mail para facilitar comparações e buscas."""
        return email.strip().lower()

    def definir_senha(self, senha: str, hasher: HashDeSenha) -> None:
        """Define a senha do usuário, gravando apenas o hash."""
        self._senha_hash = hasher.gerar(senha)

    def senha_confere(self, senha: str, hasher: HashDeSenha) -> bool:
        """Informa se a senha apresentada corresponde à cadastrada."""
        return hasher.verificar(senha, self._senha_hash)

    @validates("nome")
    def validar_nome(self, campo: str, valor: str) -> str:
        if not valor or not valor.strip():
            raise ValorInvalido("O nome do usuário não pode ficar vazio.")
        return valor.strip()

    def __repr__(self) -> str:
        return f"Usuario(id={self.id} email={self.email!r})"