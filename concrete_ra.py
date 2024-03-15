from typing import Any, Literal, override

from guards import FoodForDayExistsGuard, ValidMenuItemGuard, ValidDayStringGuard
from register_automaton import Action, OutputSymbol, RegisterAutomaton, Repository
from setup import MenuItem, WeekMenuStates, init_state, registers
from symbols import HttpException, LiteralOutputSymbol


class GetFoodForDayAction(
    Action[
        [
            Literal[
                "monday",
                "tuesday",
                "wednesday",
                "thursday",
                "friday",
                "saturday",
                "sunday",
            ]
        ],
        WeekMenuStates,
    ],
):
    @override
    def execute(
        self,
        current_state: WeekMenuStates,
        registers: dict[str, Repository[MenuItem]],
        p0: Literal[
            "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"
        ],
    ) -> tuple[OutputSymbol, WeekMenuStates]:
        match current_state:

            case WeekMenuStates.EMPTY_MENU if not ValidDayStringGuard(p0).check():
                next_state = WeekMenuStates.EMPTY_MENU
                return HttpException(400, "Bad request"), next_state

            case WeekMenuStates.EMPTY_MENU if not FoodForDayExistsGuard(p0).check():
                next_state = WeekMenuStates.EMPTY_MENU
                return HttpException(404, "Menu not found"), next_state

            case WeekMenuStates.EMPTY_MENU:
                next_state = WeekMenuStates.EMPTY_MENU
                return HttpException(404, "Menu not found"), next_state

            # ----------------

            case WeekMenuStates.PARTIAL_MENU if not ValidDayStringGuard(p0).check():
                next_state = WeekMenuStates.PARTIAL_MENU
                return HttpException(400, "Bad request"), next_state

            case WeekMenuStates.PARTIAL_MENU if not FoodForDayExistsGuard(p0).check():
                next_state = WeekMenuStates.PARTIAL_MENU
                return HttpException(404, "Menu not found"), next_state

            case WeekMenuStates.PARTIAL_MENU:
                next_state = WeekMenuStates.PARTIAL_MENU
                return LiteralOutputSymbol(registers[p0].register.food), next_state

            # ----------------

            case WeekMenuStates.FULL_MENU if not ValidDayStringGuard(p0).check():
                next_state = WeekMenuStates.FULL_MENU
                return HttpException(400, "Bad request"), next_state

            case WeekMenuStates.FULL_MENU if not FoodForDayExistsGuard(p0).check():
                next_state = WeekMenuStates.FULL_MENU
                return HttpException(404, "Menu not found"), next_state

            case WeekMenuStates.FULL_MENU:
                next_state = WeekMenuStates.FULL_MENU
                return LiteralOutputSymbol(registers[p0].register.food), next_state


class AddMenuItemAction(Action[[dict[str, Any]], WeekMenuStates]):
    @override
    def execute(
        self,
        current_state: WeekMenuStates,
        registers: dict[str, Repository[MenuItem]],
        p0: dict[str, Any],
    ) -> tuple[OutputSymbol, WeekMenuStates]:
        match current_state:
            case WeekMenuStates.EMPTY_MENU if not ValidMenuItemGuard(p0).check():
                next_state = WeekMenuStates.EMPTY_MENU
                return HttpException(400, "Bad request"), next_state

            case WeekMenuStates.EMPTY_MENU:
                next_state = WeekMenuStates.PARTIAL_MENU

                registers[p0["day"]].register = MenuItem(pk="dummy", **p0)

                return LiteralOutputSymbol(registers[p0["day"]].register), next_state

            # ----------------

            case WeekMenuStates.PARTIAL_MENU if not ValidMenuItemGuard(p0).check():
                next_state = WeekMenuStates.PARTIAL_MENU
                return HttpException(400, "Bad request"), next_state

            case WeekMenuStates.PARTIAL_MENU if registers[p0["day"]].is_null:

                next_state = WeekMenuStates.FULL_MENU

                registers[p0["day"]].register = MenuItem(pk="dummy", **p0)

                return LiteralOutputSymbol(registers[p0["day"]].register), next_state

            case WeekMenuStates.PARTIAL_MENU if not registers[p0["day"]].is_null:
                next_state = WeekMenuStates.PARTIAL_MENU

                registers[p0["day"]].register = MenuItem(pk="dummy", **p0)

                return LiteralOutputSymbol(registers[p0["day"]].register), next_state

            # ----------------

            case WeekMenuStates.FULL_MENU if not ValidMenuItemGuard(p0).check():
                next_state = WeekMenuStates.FULL_MENU
                return HttpException(400, "Bad request"), next_state

            case WeekMenuStates.FULL_MENU:
                next_state = WeekMenuStates.FULL_MENU

                registers[p0["day"]].register = MenuItem(pk="dummy", **p0)

                return LiteralOutputSymbol(registers[p0["day"]].register), next_state

            case _:
                raise Exception("Should not happen")


actions = {
    "get_food_for_day": GetFoodForDayAction(),
    "add_menu_item": AddMenuItemAction(),
}


ra = RegisterAutomaton[WeekMenuStates](
    init_state=init_state, registers=registers, actions=actions
)
