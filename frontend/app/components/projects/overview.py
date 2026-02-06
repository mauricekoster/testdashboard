from nicegui import ui
from app.components.common import Heading, TabConfig, TabsBuilder


class ActiveProjects:
    def __init__(self):
        ui.label("Active projects")


class ClosedProjects:
    def __init__(self):
        ui.label("Completed projects")


class ProjectsOverview:
    def __init__(self):
        projects_tabs = [
            TabConfig(name="active", label="Active", component=ActiveProjects),
            TabConfig(name="completed", label="Completed", component=ClosedProjects),
        ]
        TabsBuilder(projects_tabs)

