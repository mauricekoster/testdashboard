from nicegui import ui, APIRouter

from .templates.landing import landingpage

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


@router.page("/myprofile")
def show_mywork():
    final_tabs = settings_tabs[:-1] if current_user.is_superuser else settings_tabs

    with landingpage("myprofile"):

        with ui.row().classes("w-full"):
            ui.label("My profile").classes("text-h4")
            

        ui.separator()
        TabsBuilder(final_tabs)