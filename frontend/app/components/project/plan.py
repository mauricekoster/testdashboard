from nicegui import ui
from app.core.project import Project
from app.components.common import Heading


class ProjectPlan:
    def __init__(self, project: Project):

        with ui.row().classes("w-full"):
            with ui.column():
                Heading(project.name)
                Heading("Plan", "sm")
            ui.space()
            #ui.button("Manage Projects", color="secondary")

        ui.separator()
