from nicegui import ui, app

from .page_template import mainpage


def init() -> None:
    @ui.page("/items")
    def show_dashboard():
        with mainpage("Items", "items"):
            content()


def content():
    ui.label("Items")
