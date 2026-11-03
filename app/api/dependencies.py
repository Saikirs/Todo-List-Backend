"""Provedores de dependência: montam os objetos que as rotas usam.

Concentrar a montagem aqui tem um efeito prático: a rota declara que precisa
de um UsuarioServico e não sabe quantas peças existem por trás dele. Se
amanhã o serviço passar a receber um colaborador novo, muda este módulo — e
nenhuma rota.
"""

from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.config import obter_configuracao
from app.core.security import HashBcrypt, HashDeSenha, TokenJWT
from app.db.database import obter_sessao
from app.repositories import UsuarioRepositorio
from app.services import UsuarioServico


def obter_hasher() -> HashDeSenha:
    """Implementação de hash usada pela aplicação.

    Declarada como dependência — e não instanciada direto no serviço — para
    poder ser substituída nos testes por uma implementação instantânea.
    """
    return HashBcrypt()


def obter_tokens() -> TokenJWT:
    """Emissor/leitor de tokens, com o segredo e a validade da configuração."""
    config = obter_configuracao()
    return TokenJWT(config.segredo_jwt(), config.jwt_expira_minutos)


def obter_usuario_servico(
    sessao: Session = Depends(obter_sessao),
    hasher: HashDeSenha = Depends(obter_hasher),
    tokens: TokenJWT = Depends(obter_tokens),
) -> UsuarioServico:
    """Serviço de usuários, com repositório, hasher e tokens já injetados."""
    return UsuarioServico(UsuarioRepositorio(sessao), hasher, tokens)