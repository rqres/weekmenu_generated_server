from typing import Any, Literal

from concrete_ra import MenuItem, ra
from fastapi import FastAPI

app = FastAPI()


@app.get("/weekmenu")
def getFoodForDay(
    day: Literal[
        "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"
    ],
) -> str:
    """Get the menu for a specific day"""

    ra.execute("get_food_for_day", day)
    return ra.last_output.evaluate()


@app.post("/weekmenu")
def addMenuItem(request_body: dict[str, Any]) -> MenuItem:
    """Add a menu item for a specific day"""

    ra.execute("add_menu_item", request_body)
    return ra.last_output.evaluate()
