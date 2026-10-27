"""Peças comuns a todos os schemas: tradução camelCase e datas em UTC."""
from datetime import datetime, timezone
from typing import Annotated

from pydantic import AfterValidator, BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


def garantir_utc(valor: datetime) -> datetime:
    """Adiciona o fuso UTC a uma data/hora que não tem fuso. Se já tiver, não altera."""
    return valor if valor.tzinfo else valor.replace(tzinfo=timezone.utc)


# Tipo reutilizável: uma data/hora que sempre sai na resposta com o fuso.
DataHoraUTC = Annotated[datetime, AfterValidator(garantir_utc)]


class EsquemaDeEntrada(BaseModel):
    """Base dos schemas que recebem dados do cliente."""

    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)


class EsquemaDeSaida(BaseModel):
    """Base dos schemas que enviam dados para o cliente. As datas sempre saem com fuso UTC."""

    model_config = ConfigDict(
        alias_generator=to_camel, populate_by_name=True, from_attributes=True
    )