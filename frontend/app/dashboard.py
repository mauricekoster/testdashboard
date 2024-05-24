from nicegui import ui, app

from .page_template import mainpage


def init() -> None:
    @ui.page("/")
    def show_dashboard():
        with mainpage("Dashboard"):
            content()


def content() -> None:
    ui.label("Use the menu on the top right to navigate.")
    ui.label("Hello, FastAPI!")

    # NOTE dark mode will be persistent for each user across tabs and server restarts
    ui.dark_mode().bind_value(app.storage.user, "dark_mode")
    ui.checkbox("dark mode").bind_value(app.storage.user, "dark_mode")
