from contextlib import contextmanager

from .menu import main_menu

from nicegui import ui, app


@contextmanager
def mainpage(navigation_title: str):
    """Custom page frame to share the same styling and behavior across all pages"""

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
        ui.icon("account_circle")
        ui.label(app.storage.user["username"]).classes("p-2")
        ui.switch("Darkmode").bind_value(app.storage.user, "dark_mode").props(
            "flat color=accent"
        )

    with ui.left_drawer().classes("bg-blue-100") as left_drawer:
        main_menu()

    yield
