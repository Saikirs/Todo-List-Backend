"""Contrato JSON de usuário e de sessão (login)."""

from pydantic import EmailStr, Field, field_validator

from app.core.security import LIMITE_BYTES_SENHA
from app.schemas.base import DataHoraUTC, EsquemaDeEntrada, EsquemaDeSaida


class UsuarioCreate(EsquemaDeEntrada):
    """Dados recebidos no cadastro de usuário."""

    nome: str = Field(min_length=1, max_length=120)
    email: EmailStr
    senha: str = Field(min_length=6)

    @field_validator("senha")
    @classmethod
    def _senha_cabe_no_bcrypt(cls, senha: str) -> str:
        """O bcrypt só aceita até 72 bytes — conferido em BYTES, não letras."""
        if len(senha.encode("utf-8")) > LIMITE_BYTES_SENHA:
            raise ValueError(
                f"A senha pode ter no máximo {LIMITE_BYTES_SENHA} bytes."
            )
        return senha


class UsuarioLogin(EsquemaDeEntrada):
    """Credenciais recebidas no login."""

    email: EmailStr
    senha: str


class UsuarioOut(EsquemaDeSaida):
    """Dados devolvidos sobre um usuário.

    Não declara a senha nem o hash — é o schema de saída que garante que eles
    nunca saiam da API, independentemente do que exista no modelo.
    """

    id: int
    nome: str
    email: EmailStr
    criado_em: DataHoraUTC


class SessaoOut(EsquemaDeSaida):
    """Resposta do login: o token de acesso e quem está logado.

    O cliente guarda `accessToken` e o envia em toda requisição protegida, no
    cabeçalho `Authorization: Bearer <accessToken>`.
    """

    access_token: str
    token_type: str = "bearer"
    expira_em: DataHoraUTC
    usuario: UsuarioOut