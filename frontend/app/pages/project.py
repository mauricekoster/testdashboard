from nicegui import ui, APIRouter

from .templates.project import projectpage
from app.core.project import Project

router = APIRouter()


@router.page("/project/{projectId}")
def show_projects(projectId):
    project = Project(projectId)
    with projectpage(project, "dashboard"):
        content()


def content() -> None:
    with ui.row().classes("w-full"):
        ui.label("Project").classes("text-h4")
        ui.space()
        #ui.button("Manage Projects", color="secondary")

    ui.separator()


    
