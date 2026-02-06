from contextlib import contextmanager

from app.components.menu import UserDropdownMenu
from app.core.config import settings

from nicegui import ui, app
from app.core.user import current_user
from app.components.navbar import NavBar, NavBarItem


nav_items = [
    NavBarItem("oldhome", "Old home", "/home"),
    NavBarItem("projects", "Projects", "/projects"),
    NavBarItem("mywork", "My Work", "/mywork")
]


@contextmanager
def landingpage(active_menu: str):
    """Custom page frame to share the same styling and behavior across all pages"""

    current_user.check()

    ui.dark_mode().bind_value(app.storage.user, "dark_mode")
    ui.colors(
        primary="#5E81AC", secondary="#88C0D0", accent="#8FBCBB", positive="#53B689"
    )
    with ui.header().classes(replace="row items-center"):
        ui.button(icon="home").props(
            "flat color=white"
        )
        ui.label(settings.PROJECT_NAME).classes("font-bold mr-5")
        
        NavBar(nav_items, active_menu)

        ui.space()
        if current_user.is_superuser:
            with ui.link(target="/settings"):
                ui.button(icon="settings").props(
                    "flat color=white"
                )

        UserDropdownMenu()

    with ui.column().classes("w-full p-5"):
        yield
