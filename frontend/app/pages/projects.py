from nicegui import ui, APIRouter

from .template import mainpage
from .menus import main_menu

router = APIRouter()


@router.page("/projects")
def show_projects():
    with mainpage("Projects", main_menu, "projects"):
        content()


columns = [
    {
        "name": "name",
        "label": "Name",
        "field": "name",
        "required": True,
        "align": "left",
    },
    {"name": "latest", "label": "Latest", "field": "latest", "sortable": True},
    {"name": "current", "label": "Current", "field": "current", "sortable": True},
]
projects = [
    {"name": "First project", "latest": "FAIL", "current": "PASS"},
]


def content() -> None:
    ui.label("Projects here...")
    ui.button("Create project")
    ui.separator()
    with ui.column().classes("w-full"):
        # with ui.card().style("width: 100%").tight():
        with ui.card().classes("w-full").tight():
            with ui.card_section().classes("w-full"):
                with ui.row().classes("w-full"):
                    ui.label("Test").classes("text-h6")
                    ui.space()
                    ui.label("Description of the project...")
                    ui.space()
                    ui.badge("OK")
            with ui.card_actions().classes("w-full").props("align='right'"):
                ui.button("Test 1")
                ui.button("Test 2")
        ui.card()

    ui.table(columns=columns, rows=projects, row_key="name")
    ui.label("Latest: latest results. Current: results from current release.")
