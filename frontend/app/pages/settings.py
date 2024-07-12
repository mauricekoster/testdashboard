from nicegui import APIRouter

from .template import mainpage

from .menus import main_menu

from app.components.user_settings import (
    Appearance,
    ChangePassword,
    UserInformation,
    DeleteAccount,
)
from app.components.common import Heading, TabConfig, TabsBuilder

from app.core.user import current_user

router = APIRouter()

settings_tabs = [
    TabConfig(name="myprofile", label="My profile", component=UserInformation),
    TabConfig(name="changepassword", label="Password", component=ChangePassword),
    TabConfig(name="appearance", label="Appearance", component=Appearance),
    TabConfig(name="deleteaccount", label="Danger zone", component=DeleteAccount),
]


@router.page("/settings")
def show_dashboard():
    final_tabs = settings_tabs[:-1] if current_user.is_superuser else settings_tabs

    with mainpage("User settings", main_menu, "settings"):
        Heading("User settings")
        TabsBuilder(final_tabs)
