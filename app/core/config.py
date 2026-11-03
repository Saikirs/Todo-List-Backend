"""Configuração da aplicação, a partir de variáveis de ambiente.
"""
from __future__ import annotations
import os
from dataclasses import dataclass
from functools import lru_cache
from dotenv import load_dotenv
load_dotenv()
class ConfiguracaoInvalida(RuntimeError):
    """Falta (ou está errada) uma variável de ambiente obrigatória."""
@dataclass(frozen=True)
class Configuracao:
    """Parâmetros de execução da aplicação."""
    database_url: str = ""
    jwt_secret: str = ""
    jwt_expira_minutos: int = 120
    @classmethod
    def do_ambiente(cls) -> Configuracao:
        """Monta a configuração a partir das variáveis de ambiente."""
        return cls(
            database_url=os.getenv("DATABASE_URL", "").strip(),
            jwt_secret=os.getenv("JWT_SECRET", ""),
            jwt_expira_minutos=int(os.getenv("JWT_EXPIRA_MINUTOS", "120")),
        )
    @property
    def url_banco(self) -> str:
        """Devolve a URL do banco de dados, ou levanta ConfiguracaoInvalida."""
        if not self.database_url:
            raise ConfiguracaoInvalida(
                "DATABASE_URL não definida. Copie o arquivo .env. example para .env"
                "e deixe ativo um dos dois caminhos: SQLite (local) ou PostgreSQL no Render."
            )
        return self.database_url
    def segredo_jwt(self) -> str:
        """Devolve a variável de ambiente JWT_SECRET, ou explica como criá-la."""
        if len(self.jwt_secret) < 32:
            raise ConfiguracaoInvalida(
                "JWT_SECRET ausente ou curto demais (mínimo 32 caracteres)."
                "Gere um com: python -c \"import secrets; print(secrets.token_hex(32))\" "
                "e coloque no arquivo .env."
            )
        return self.jwt_secret
@lru_cache
def obter_configuracao() -> Configuracao:
    """Devolve a configuração da aplicação, carregada uma única vez."""
    return Configuracao.do_ambiente()