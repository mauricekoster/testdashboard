from nicegui import ui, APIRouter

from .templates.landing import landingpage
from .menus import main_menu

router = APIRouter()


@router.page("/mywork")
def show_mywork():
    with landingpage("mywork"):

        with ui.row().classes("w-full"):
            ui.label("My Work").classes("text-h4")
            

        ui.separator()
    