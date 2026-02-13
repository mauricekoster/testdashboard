from nicegui import ui
from app.core.project import Project
from app.components.common import Heading, TabConfig, TabsBuilder


class RequirementsMain():
    def __init__(self):
        with ui.row().classes("w-full"):
            ui.space()
            ui.button(icon="more_horiz", color="secundary").props("outline")
            ui.button("Add requirement...", color="primary").props("no-caps")

        with ui.row().classes("w-full"):
            with ui.card().classes("w-full"):
                ui.label("Requirements here")


class RisksMain():
    def __init__(self):
        with ui.row().classes("w-full"):
            ui.space()
            ui.button(icon="more_horiz", color="secundary").props("outline")
            ui.button("Add risk...", color="primary").props("no-caps")

        with ui.row().classes("w-full"):
            with ui.card().classes("w-full"):
                ui.label("Risks here")




class ProjectDefine:
    def __init__(self, project: Project):

        tabs = [

            TabConfig(name="requirements", label="Requirements", component=RequirementsMain),
            TabConfig(name="risks", label="Risks", component=RisksMain),
        ]
        TabsBuilder(tabs)


