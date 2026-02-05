from nicegui import APIRouter, ui
from .app_menu import application_menu
from app.pages.template import frame
from app.components.common import Heading

from app.components.settings import ApplicationInformation, ApplicationGroups, ApplicationMatrix


router = APIRouter(prefix="/app")

@router.page("/{app_id}/settings")
def application_settings(app_id: str):

    

    with frame(f"- Application {app_id} settings-", application_menu(app_id), "app-settings"):
        Heading("Settings")

        with ui.tabs().props('align=left').classes('w-full') as tabs:
            application_information = ui.tab('Application')
            application_groups = ui.tab('Groups')
            application_matrix = ui.tab('Matrix')
        with ui.tab_panels(tabs, value=application_information).classes('w-full'):
            with ui.tab_panel(application_information):
                ApplicationInformation(app_id)
            with ui.tab_panel(application_groups):
                ApplicationGroups(app_id)
            with ui.tab_panel(application_matrix):
                ApplicationMatrix(app_id)
