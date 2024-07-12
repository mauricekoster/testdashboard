from pydantic import BaseModel
from typing_extensions import Any
from nicegui import ui


class TabConfig(BaseModel):
    name: str
    label: str
    component: Any


class TabsBuilder:
    def __init__(self, tabs_config: list[TabConfig], dense: bool = False) -> None:
        with ui.tabs().props("no-caps align=left").classes("w-full") as self.tabs:
            for tab in tabs_config:
                ui.tab(name=tab.name, label=tab.label)

        with ui.tab_panels(self.tabs, value=tabs_config[0].name).classes("w-full"):
            for tab in tabs_config:
                with ui.tab_panel(tab.name):
                    tab.component()

        if dense:
            self.tabs.props(add="dense")

    def dense(self):
        self.tabs.props(add="dense")
