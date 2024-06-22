from nicegui import ui, app

from .template import mainpage
from .menus import main_menu


def init() -> None:
    @ui.page("/items")
    def show_dashboard():
        with mainpage("Items", main_menu, "items"):
            content()


def content():
    ui.label("Items")
