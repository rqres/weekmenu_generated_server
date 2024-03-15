from typing import Any, Callable, override

from fastapi import HTTPException
from register_automaton import ArrayRepository, OutputSymbol

# **** built-ins ****

class LiteralOutputSymbol(OutputSymbol):
    def __init__(self, value: Any) -> None:
        self.value = value

    @override
    def evaluate(self) -> Any:
        return self.value

class HttpException(OutputSymbol):
    def __init__(self, p0: int, p1: str) -> None:
        self.p0 = p0
        self.p1 = p1

    @override
    def evaluate(self) -> HTTPException:
        return HTTPException(status_code=self.p0, detail=self.p1)


class FilteredList(OutputSymbol):
    def __init__(
        self, p0: ArrayRepository[Any], p1: Callable[[Any], bool] | None
    ) -> None:
        self.p0 = p0
        self.p1 = p1

    @override
    def evaluate(self) -> list[Any]:
        if not self.p1:
            return self.p0.register

        return [el for el in self.p0.register if self.p1(el)]

class LastEntry(OutputSymbol):
    def __init__(self, p0: ArrayRepository[Any]) -> None:
        self.p0 = p0

    @override
    def evaluate(self) -> Any:
        return self.p0.register[-1]


# **** end built-ins ****

class EmptyList(OutputSymbol):
    @override
    def evaluate(self) -> list[Any]:
        return []
