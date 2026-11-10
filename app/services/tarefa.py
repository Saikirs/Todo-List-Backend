"""Operações sobre as tarefas do usuário autenticado."""

from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from typing import Any
from app.core.exceptions import AcessoNaoAutorizado, TarefaNaoEncontrada
from app.models import Tarefa
from app.models.enums import PrioridadeTarefa
from app.repositories import TarefaRepositorio


NAO_INFORMADO: Any = object()
@dataclass(frozen=True)
class AlteracoesDaTarefa:
    """Campos que um PATCH pediu para alterar."""
    titulo: Any = NAO_INFORMADO
    prioridade: Any = NAO_INFORMADO
    prazo: Any = NAO_INFORMADO
    def informado(self, campo: str) -> bool:
        """Informa se o cliente enviou este campo."""
        return getattr(self, campo) is not NAO_INFORMADO

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
    
    def buscar(self, tarefa_id: int, usuario_id: int) -> Tarefa:
        """Devolve uma tarefa do usuário."""
        tarefa = self._tarefas.buscar_por_id(tarefa_id)
        if tarefa is None:
            raise TarefaNaoEncontrada()
        if not tarefa.pertence_a(usuario_id):
            raise AcessoNaoAutorizado()
        return tarefa
    
    def atualizar(
        self, tarefa_id: int, usuario_id: int, alteracoes: AlteracoesDaTarefa
    ) -> Tarefa:
        """Aplica as alterações informadas e devolve a tarefa atualizada."""
        tarefa = self.buscar(tarefa_id, usuario_id)
        if alteracoes.informado("titulo"):
            tarefa.titulo = alteracoes.titulo
        if alteracoes.informado("prioridade"):
            tarefa.prioridade = alteracoes.prioridade
        if alteracoes.informado("prazo"):
            tarefa.prazo = alteracoes.prazo
        return self._tarefas.salvar(tarefa)
    
    def remover(self, tarefa_id: int, usuario_id: int) -> None:
        """Remove a tarefa definitivamente."""
        self._tarefas.remover(self.buscar(tarefa_id, usuario_id))