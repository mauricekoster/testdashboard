from contextlib import contextmanager

from app.components.menu import display_menu

from nicegui import ui, app
from app.core.user import current_user


@contextmanager
def detailpage(navigation_title: str, menu: dict, active_menu: str):
    """Custom page frame to share the same styling and behavior across all pages"""

    current_user.check()

    ui.dark_mode().bind_value(app.storage.user, "dark_mode")
    ui.colors(
        primary="#5E81AC", secondary="#88C0D0", accent="#8FBCBB", positive="#53B689"
    )
    with ui.header().classes(replace="row items-center"):
        ui.button(on_click=lambda: left_drawer.toggle(), icon="menu").props(
            "flat color=white"
        )
        ui.label("Test Dashboard").classes("font-bold")
        ui.space()
        ui.label(navigation_title)
        ui.space()
        with ui.dropdown_button(
            app.storage.user["username"], icon="account_circle", auto_close=True
        ).props("rounded no-caps").classes("q-ma-sm"):
            ui.item("My profile", on_click=lambda: ui.navigate.to("/settings"))
            ui.item("Log out", on_click=lambda: ui.navigate.to("/logout"))
            ui.switch("Darkmode").bind_value(app.storage.user, "dark_mode").props(
                "flat"
            )

    with ui.left_drawer(bordered=True) as left_drawer:
        display_menu(menu_definition=menu, active_menu=active_menu)

    with ui.column().classes("w-full"):
        yield
