"""Acesso aos dados de tarefa."""

from __future__ import annotations

from app.models import Tarefa
from app.repositories.base import RepositorioBase

class TarefaRepositorio(RepositorioBase[Tarefa]):
    """Acesso aos dados de tarefa."""

    @property
    def modelo(self) -> type[Tarefa]:
        return Tarefa

    def listar(self, usuario_id: int) -> list [Tarefa]:
        """Lista as tarefas de um usuário, das mais recentes para as mais antigas.

        O filtro pelo dono vai na consulta - no `WHERE` -, e não num `if` depois
        de buscar tudo: o banco devolve só o que é do usuário.
        """
        return (
            self._sessao.query(Tarefa)
            .filter(Tarefa.usuario_id == usuario_id)
            # Desempate pelo id: tarefas criadas no mesmo instante saem
            # sempre na mesma ordem.
            .order_by(Tarefa.criado_em.desc(), Tarefa.id.desc())
            .all()
        )