"""Schemas Pydantic: o contrato de entrada e saída da API.

Aqui mora a tradução entre dois mundos de nomenclatura. O Python escreve
`criado_em`; o JSON que o front-end consome espera `criadoEm`. A conversão
acontece na borda — que é o lugar ideal: o domínio fala Python idiomático e
estes schemas fazem a tradução automaticamente, pelo alias generator.
`populate_by_name=True` mantém a compatibilidade: a API aceita tanto o nome em
camelCase quanto o nome em Python na entrada.
"""

from app.schemas.base import DataHoraUTC, EsquemaDeEntrada, EsquemaDeSaida
from app.schemas.usuario import UsuarioCreate, UsuarioOut

__all__ = [
    "DataHoraUTC",
    "EsquemaDeEntrada",
    "EsquemaDeSaida",
    "UsuarioCreate",
    "UsuarioOut",
]