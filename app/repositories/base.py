"""Base comum a todos os repositórios."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from sqlalchemy.orm import Session

Entidade = TypeVar("Entidade")


class RepositorioBase(ABC, Generic[Entidade]):
    """Operações comuns a qualquer repositório.

    Classe abstrata que funciona como interface: obriga cada repositório
    concreto a declarar qual modelo administra e, em troca, entrega prontas as
    operações que não mudam de entidade para entidade. É herança usada para o
    que ela serve — eliminar repetição real, não para criar hierarquia.
    """

    def __init__(self, sessao: Session) -> None:
        self._sessao = sessao

    @property
    @abstractmethod
    def modelo(self) -> type[Entidade]:
        """Classe do modelo administrado por este repositório."""

    def buscar_por_id(self, identificador: int) -> Entidade | None:
        """Devolve a entidade com o id informado, ou None."""
        return self._sessao.get(self.modelo, identificador)

    def salvar(self, entidade: Entidade) -> Entidade:
        """Persiste a entidade e deixa-a sincronizada com o banco."""
        self._sessao.add(entidade)
        self._sessao.commit()
        self._sessao.refresh(entidade)
        return entidade

    def remover(self, entidade: Entidade) -> None:
        """Apaga a entidade definitivamente."""
        self._sessao.delete(entidade)
        self._sessao.commit()