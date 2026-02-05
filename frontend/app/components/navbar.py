from dataclasses import dataclass
from nicegui import ui

@dataclass
class NavBarItem:
    name: str
    title: str
    target: str

    def __call__(self, active="*none*"):
        color = "white" if self.name == active else "secondary"

        with ui.link(target=self.target):
            ui.button(self.title).props(
                f"outline rounded no-caps align='left' color='{color}'"
            ).classes('mx-1')

# ui.button("My Work").props(
        #     "outline rounded no-caps color=accent"
        # ).classes("mx-1")

class NavBar():
    def __init__(self, narbar_items: list[NavBarItem], active_item: str):
        for item in narbar_items:
            item(active_item)