from typing import Any, override

from register_automaton import Guard
from setup import registers


class ValidMenuItemGuard(Guard):
    def __init__(self, req_body: dict[str, Any]):
        self.req_body = req_body

    @override
    def check(self) -> bool:
        cond1 = self.req_body["day"] in [
            "monday",
            "tuesday",
            "wednesday",
            "thursday",
            "friday",
            "saturday",
            "sunday",
        ]
        cond2 = self.req_body["food"] != ""

        return cond1 and cond2


class FoodForDayExistsGuard(Guard):
    def __init__(self, day: str):
        self.day = day

    @override
    def check(self) -> bool:
        cond1 = not registers[self.day].is_null

        return cond1
