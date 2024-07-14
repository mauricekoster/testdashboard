from nicegui import ui, app, APIRouter

from .template import mainpage
from .menus import main_menu
from app.core.user import current_user

router = APIRouter()


@router.page("/")
def show_dashboard():
    with mainpage("Dashboard", main_menu, "dashboard"):
        ui.label("Use the menu on the left to navigate.")
        ui.label(f"Hi, {current_user.full_name or current_user.email} 👋🏼")
        ui.label("Welcome back, nice to see you again!")
