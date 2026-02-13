from nicegui import ui
from app.core.project import Project
from app.components.common import Heading


class ProjectDashboard:
    def __init__(self, project: Project):
        with ui.row().classes("w-full"):
            ui.link("< Projects", "/projects").classes("!no-underline text-green")
        with ui.row().classes("w-full"):
            Heading(project.name)
            ui.space()
            #ui.button("Manage Projects", color="secondary")

        ui.separator()
