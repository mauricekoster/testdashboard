from nicegui import ui, app

from .template import mainpage
from .menus import main_menu
from ..login import current_user


def init() -> None:
    @ui.page("/")
    def show_dashboard():
        with mainpage("Dashboard", main_menu, "dashboard"):
            content()


def content() -> None:
    ui.label("Use the menu on the left to navigate.")
    ui.label(f"Hi, {current_user.full_name or current_user.email} 👋🏼")
    ui.label("Welcome back, nice to see you again!")
