from contextlib import contextmanager

from app.components.menu import display_menu
from app.core.config import settings

from nicegui import ui, app
from app.core.user import current_user


@contextmanager
def landingpage(navigation_title: str, menu: dict, active_menu: str):
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
        
        ui.button("Projects").props(
            "outline rounded no-caps color=secundary"
        ).classes("mx-1")
        ui.button("My Work").props(
            "outline rounded no-caps color=accent"
        ).classes("mx-1")

        ui.space()
        ui.button(icon="settings").props(
            "flat color=white"
        )
        with ui.dropdown_button(
            app.storage.user["username"], icon="account_circle", auto_close=True
        ).props("rounded no-caps").classes("q-ma-sm"):
            ui.item("My profile", on_click=lambda: ui.navigate.to("/settings"))
            ui.item("Log out", on_click=lambda: ui.navigate.to("/logout"))
            ui.switch("Darkmode").bind_value(app.storage.user, "dark_mode").props(
                "flat"
            )

    with ui.column().classes("w-full p-5"):
        yield
