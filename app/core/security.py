"""Segurança: funções de hash de senha e verificação de hash.
"""
from __future__ import annotations
from abc import ABC, abstractmethod
import bcrypt
LIMITE_BYTES_SENHA = 72
class HashDeSenha(ABC):
    """Contrato de implementação de hash de senha. A aplicação só usa a interface, não
    """
    @abstractmethod
    def gerar(self, senha: str) -> str:
        """Devolve o hash da senha informada."""
    @abstractmethod
    def verificar(self, senha: str, hash_armazenado: str) -> bool:
        """Confere se a senha corresponde ao hash gravado."""
class HashBcrypt(HashDeSenha):
    """Implementação de senha usando o algoritmo bcrypt.
    """
    def gerar(self, senha: str) -> str:
        return bcrypt.hashpw(senha.encode("utf-8"), bcrypt.gensalt()).decode("ascii")
    def verificar(self, senha: str, hash_armazenado: str) -> bool:
        """Confere se a senha corresponde ao hash gravado."""
class HashBcrypt(HashDeSenha):
    """Implementação de hash de senha usando o algoritmo bcrypt.
    """
    def gerar(self, senha: str) -> str:
        return bcrypt.hashpw(senha.encode("utf-8"), bcrypt.gensalt()).decode("ascii")
    def verificar(self, senha: str, hash_armazenado: str) -> bool:
        senha_bytes = senha.encode("utf-8")
        if len(senha_bytes) > LIMITE_BYTES_SENHA:
            return False
        return bcrypt.checkpw(senha_bytes, hash_armazenado.encode("ascii"))