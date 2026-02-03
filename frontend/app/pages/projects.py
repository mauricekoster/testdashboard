from nicegui import ui, APIRouter

from .templates.landing import landingpage
from app.components.projects import ProjectsOverview


router = APIRouter()


@router.page("/projects")
def show_projects():
    with landingpage("projects"):
        content()


def content() -> None:
    with ui.row().classes("w-full"):
        ui.label("Projects").classes("text-h4")
        ui.space()
        ui.button("Manage Projects", color="secondary")

    ui.separator()
    ProjectsOverview()

    
