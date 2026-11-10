"""Operações sobre as tarefas do usuário autenticado."""

from __future__ import annotations

from datetime import date

from app.models import Tarefa
from app.models.enums import PrioridadeTarefa
from app.repositories import TarefaRepositorio


class TarefaServico:
    """Operações sobre as tarefas do usuário autenticado.

    Toda operação recebe o id de quem está pedindo. Isso não é desconfiança
    exagerada: é a única forma de garantir que ninguém leia, altere ou apague
    a tarefa de outra pessoa só por adivinhar um id.
    """

    def __init__(self, tarefas: TarefaRepositorio) -> None:
        self._tarefas = tarefas

    def criar(
        self,
        usuario_id: int,
        titulo: str,
        prioridade: PrioridadeTarefa,
        prazo: date | None,
    ) -> Tarefa:
        """Cria uma tarefa para o usuário autenticado.

        """
        tarefa = Tarefa(
            usuario_id=usuario_id,
            titulo=titulo,
            prioridade=prioridade,
            prazo=prazo,
        )

        return self._tarefas.salvar(tarefa)

    def listar(self, usuario_id: int) -> list[Tarefa]:
        """Lista as tarefas do usuário autenticado."""
        return self._tarefas.listar(usuario_id)