from enum import Enum, auto
from typing import Any, Literal

from register_automaton import Entity, Repository


class WeekMenuStates(Enum):
    EMPTY_MENU = auto()
    PARTIAL_MENU = auto()
    FULL_MENU = auto()


class MenuItem(Entity):
    day: Literal[
        "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"
    ]
    food: str


registers: dict[str, Repository[Any]] = {
    "monday": Repository[MenuItem](MenuItem(pk="dummy", day="monday", food="")),
    "tuesday": Repository[MenuItem](MenuItem(pk="dummy", day="tuesday", food="")),
    "wednesday": Repository[MenuItem](MenuItem(pk="dummy", day="wednesday", food="")),
    "thursday": Repository[MenuItem](MenuItem(pk="dummy", day="thursday", food="")),
    "friday": Repository[MenuItem](MenuItem(pk="dummy", day="friday", food="")),
    "saturday": Repository[MenuItem](MenuItem(pk="dummy", day="saturday", food="")),
    "sunday": Repository[MenuItem](MenuItem(pk="dummy", day="sunday", food="")),
}

init_state = WeekMenuStates.EMPTY_MENU
