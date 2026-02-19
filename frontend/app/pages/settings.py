from nicegui import APIRouter, ui

from .templates.landing import landingpage

from app.components.common import Heading
from app.components.menu import menu_item

router = APIRouter()

from collections import OrderedDict

settings_menu = OrderedDict([
    ("General", [
        dict(name='account', title='Account', link='/settings', icon='supervisor_account'),
        dict(name='other', title='Other..', link='/settings/other', icon='miscellaneous_services'),
    ]),
    ("Projects & Tests", [
        
    ]),
    ("Access & Security", [
        dict(name='account', title='Users', link='/settings/users', icon='supervisor_account'),
    ]),
    ("Integrations & Data", [
        
    ]),
])


active = None




@router.page("/settings")
@router.page('/settings/{_:path}')
class SettingsPage():
    def __init__(self):
        self.active = 'account'
        with landingpage("settings"):
            
            with ui.row().classes("w-full"):
                Heading("Settings")
            ui.separator()

            with ui.row().classes("flex w-full"):
                with ui.column().classes("flex w-1/6"):
                    
                    self.menu()

                with ui.column().classes("flex w-4/5"):

                    ui.sub_pages(
                        {
                            '/settings': self.settings_general, 
                            '/settings/other': self.settings_other
                        }
                    ).classes('w-full')

    @ui.refreshable
    def menu(self):
        for k, v in settings_menu.items():
            Heading(k, "xs")
            for item in v:
                menu_item(item['title'], item['link'], icon=item['icon'], is_active=(item['name']==self.active))

    def settings_general(self):
        with ui.card().classes("w-full"):
            ui.label("General")
            self.active = 'account'
            self.menu.refresh()
            

    def settings_other(self):
        with ui.card().classes("w-full"):
            ui.label("Other")
            self.active = 'other'
            self.menu.refresh()