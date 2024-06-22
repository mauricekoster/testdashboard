from nicegui import ui, app

from .template import mainpage
from .menus import main_menu


def init() -> None:
    @ui.page("/settings")
    def show_dashboard():
        with mainpage("User settings", main_menu, "settings"):
            content()


def content():
    ui.label("User settings")
