from nicegui import ui, APIRouter

from .template import mainpage
from .menus import main_menu


router = APIRouter()


@router.page("/settings")
def show_dashboard():
    with mainpage("User settings", main_menu, "settings"):
        content()


def content():
    ui.label("User settings")
