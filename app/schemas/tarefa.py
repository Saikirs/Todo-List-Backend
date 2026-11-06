"""Contrato JSON de tarefa."""

from datetime import date

from pydantic import Field

from app.models.enums import PrioridadeTarefa, StatusTarefa
from app.schemas.base import DataHoraUTC, EsquemaDeEntrada, EsquemaDeSaida


# ------------------------------------------------------------ Tarefa

class TarefaCreate(EsquemaDeEntrada):
    """Dados recebidos na criação de uma tarefa.

    Não há `usuarioId`: o dono é sempre quem está autenticado. O status
    também não é aceito: toda tarefa nasce pendente (RN-02).
    """

    titulo: str = Field(min_length=1, max_length=200)
    prioridade: PrioridadeTarefa = PrioridadeTarefa.MEDIA
    prazo: date | None = None


class TarefaOut(EsquemaDeSaida):
    """Representação completa de uma tarefa nas respostas da API."""

    id: int
    usuario_id: int
    titulo: str
    status: StatusTarefa
    prioridade: PrioridadeTarefa
    prazo: date | None
    criado_em: DataHoraUTC
    atualizado_em: DataHoraUTC
    concluido_em: DataHoraUTC | None