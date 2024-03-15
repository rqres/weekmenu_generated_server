from abc import ABC, abstractmethod
from typing import Any, Mapping

from fastapi import HTTPException
from pydantic import BaseModel


class Entity(BaseModel):
    pk: str


class Repository[T]:
    """
    Repository: Each Repo defines CRUD operations for a specific entity.
    It also defines the entity's associated register.
    """

    def __init__(self, value: T):
        self._register = value
        self.is_null = True

    @property
    def register(self) -> T:
        return self._register

    @register.setter
    def register(self, register: T) -> None:
        self._register = register
        self.is_null = False

    def __repr__(self) -> str:
        return f"<{type(self).__name__} {self.register}>"


class ArrayRepository[T](Repository[list[T]]):
    def __init__(self, value: list[T] | None = None) -> None:
        if value is None:
            value = []

        super().__init__(value)

    def __get_item__(self, index: int) -> T:
        if index >= len(self.register):
            raise IndexError("Index out of range")

        return self.register[index]

    def __contains__(self, item: T) -> bool:
        return item in self.register

    def add(self, item: T) -> T | None:
        if item in self.register:
            return None

        self.register.append(item)
        return item

    def delete(self, item: T) -> None:
        if item in self.register:
            self.register.remove(item)


class OutputSymbol(ABC):
    @abstractmethod
    def evaluate(self) -> Any:
        return None




class Guard(ABC):
    @abstractmethod
    def check(self) -> bool:
        pass


class Action[**P, S](ABC):
    @abstractmethod
    def execute(
        self,
        current_state: S,
        registers: dict[str, Repository[Any]],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> tuple[OutputSymbol, S]:
        pass


class RegisterAutomaton[S]:
    def __init__(
        self,
        *,
        init_state: S,
        registers: dict[str, Repository[Any]],
        actions: Mapping[str, Action[Any, S]],
    ) -> None:
        self.registers = registers
        self.init_state = init_state
        self.actions = actions

        self.current_state = self.init_state

    def execute(self, operation_name: str, *args: Any, **kwargs: Any) -> None:
        action = self.actions.get(operation_name)

        if action is not None:
            self.last_output, next_state = action.execute(
                self.current_state, self.registers, *args, **kwargs
            )

            self.current_state = next_state

            if isinstance(self.last_output.evaluate(), HTTPException):
                raise self.last_output.evaluate()

            return

        raise ValueError
