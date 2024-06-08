from nicegui import ui, app

from .page_template import mainpage


def init() -> None:
    @ui.page("/settings")
    def show_dashboard():
        with mainpage("User settings", "settings"):
            content()


def content():
    ui.label("User settings")
