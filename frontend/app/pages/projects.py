from nicegui import ui, APIRouter

from .templates.landing import landingpage
from app.components.projects import ProjectsOverview
from app.components.project.add import ProjectAdd

router = APIRouter()


@router.page("/projects")
def show_projects():
    with landingpage("projects"):
        content()


def content() -> None:
    with ui.row().classes("w-full"):
        ui.label("Projects").classes("text-h4")
        ui.space()
        ui.button("Add project", color="secondary", on_click=on_handle_add)
        ui.button("Manage Projects", color="secondary")

    ui.separator()
    project_overview()

@ui.refreshable
def project_overview():
    ProjectsOverview()

    

async def on_handle_add():
    add_dialog = ProjectAdd(project_overview)
    await add_dialog.show()