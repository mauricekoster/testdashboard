from nicegui import ui, APIRouter

from .template import mainpage
from .menus import main_menu

router = APIRouter()


@router.page("/items")
def show_dashboard():
    with mainpage("Items", main_menu, "items"):
        content()


def content():
    ui.label("Items")
