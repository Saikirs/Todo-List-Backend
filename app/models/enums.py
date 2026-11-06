"""Enumerações do domínio.

Antes, os valores válidos de status e prioridade estavam escritos como texto
solto em três lugares: no `Literal` dos schemas, no `default`das colunas e no
`case` que ordenava por prioridade. Acrescentar uma prioridade nova exigia
lembrar dos três. Aqui eles passam a ter um único lugar de definição.

Herdar de `str` faz cada membro se comportar como o próprio texto - o que
permite gravá-lo em uma coluna `String`, compará-lo com uma string vinda do banco e serializá-lo em JSON sem conversão manual.
"""
from enum import Enum

class StatusTarefa(str, Enum):
    """Situação em que uma tarefa pode estar."""

    PENDENTE = "pendente"
    CONCLUIDA = "concluida"

class PrioridadeTarefa(str, Enum):
    """Nível de prioridade de uma tarefa, da menor para a maior."""

    BAIXA = "baixa"
    MEDIA = "media"
    ALTA = "alta"
    URGENTE = "urgente"
    @property
    def peso(self) -> int:
        """Posição na ordenação por prioridade - 0 é a mais urgente.
        Ordenar pelo texto daria "alta, baixa, media, urgente", que não é a ordem que o usuário espera ver. O peso existe para isso.
        """
        return _PESOS[self]
    @classmethod
    def mapa_de_pesos(cls) -> dict[str, int]:
        """Mapa `valor -> peso`, no formato que o `case()` do SQL consome."""
        return {prioridade.value: prioridade.peso for prioridade in cls}
_PESOS = {
    PrioridadeTarefa.URGENTE: 0,
    PrioridadeTarefa.ALTA: 1,
    PrioridadeTarefa.MEDIA: 2,
    PrioridadeTarefa.BAIXA: 3,
}