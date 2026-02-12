from contextlib import contextmanager
from functools import partial

from app.components.menu import UserDropdownMenu
from app.core.config import settings

from nicegui import ui, app
from app.core.user import current_user
from app.core.project import Project

from app.components.navbar import NavBar, NavBarItem
from app.client.projects import read_projects

nav_items = [
    NavBarItem("define", "Define", "/project/:id/define"),
    NavBarItem("design", "Design", "/project/:id/design"),

]


@contextmanager
def projectpage(project: Project, active_menu: str):
    """Custom page frame to share the same styling and behavior across all pages"""

    current_user.check()

    projects = read_projects()

    ui.dark_mode().bind_value(app.storage.user, "dark_mode")
    ui.colors(
        primary="#5E81AC", secondary="#88C0D0", accent="#8FBCBB", positive="#53B689"
    )
    with ui.header().classes(replace="row items-center"):
        ui.button(icon="home").props(
            "flat color=white"
        )
        ui.label(settings.PROJECT_NAME).classes("font-bold mr-5")
        
        for n in nav_items:
            n.target = n.target.replace(':id', str(project.id))
        NavBar(nav_items, active_menu)

        ui.space()
        ui.icon('o_search', size='sm')
        with ui.dropdown_button(project.name, auto_close=True).props("no-caps").classes("mx-2"):
            with ui.row().classes("items-center w-full p-3"):
                ui.label(project.name).classes("text-bold")
                ui.space()
                ui.icon("settings", size="xs")
            ui.separator()
            for p in projects.data:
                if p.name != project.name:
                    ui.item(p.name, on_click=partial(ui.navigate.to, f"/project/{p.id}"))
            ui.separator()
            ui.item("View all projects...", on_click=lambda: ui.navigate.to("/"))

        if current_user.is_superuser:
            with ui.link(target="/settings"):
                ui.button(icon="settings").props(
                    "flat color=white"
                )

        UserDropdownMenu()

    with ui.column().classes("w-full p-5"):
        yield
