from nicegui import APIRouter, ui

from .templates.landing import landingpage

from app.components.common import Heading
from app.components.menu import menu_item
from app.components.projects import ProjectsManagement
from app.components.users import UserManagement


router = APIRouter()

from collections import OrderedDict

settings_menu = OrderedDict([
    ("General", [
        dict(name='account', title='Account', link='/settings', icon='supervisor_account'),
        #dict(name='branding', title='Branding', link='/settings/nyi', icon='style'),
        #dict(name='billing', title='Billing', link='/settings/nyi', icon='credit_card'),
    ]),
    ("Projects & Tests", [
        dict(name='projects', title='Projects', link='/settings/projects', icon='assignment'), 
        #dict(name='applications', title='Applications', link='/settings/nyi', icon='not_listed_location'), 
        #dict(name='templates', title='Templates', link='/settings/nyi', icon='not_listed_location'), 
        #dict(name='environments', title='Environments', link='/settings/nyi', icon='not_listed_location'), 
    ]),
    ("Access & Security", [
        dict(name='users', title='Users', link='/settings/users', icon='supervisor_account'),
        #dict(name='teams', title='Teams', link='/settings/nyi', icon='supervisor_account'),
        #dict(name='roles', title='Roles', link='/settings/nyi', icon='supervisor_account'),
        #dict(name='auditlog', title='Audit Log', link='/settings/nyi', icon='supervisor_account'),
        #dict(name='singlesignon', title='Single Sign On', link='/settings/nyi', icon='supervisor_account'),
        #dict(name='twofactorauth', title='Two Factor Authentication', link='/settings/users', icon='supervisor_account'),
    ]),
    ("Integrations & Data", [
        dict(name='integrations', title='Integrations', link='/settings/nyi', icon='not_listed_location'), 
    ]),
])



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

                with ui.column().classes("flex w-4/5 mt-10"):

                    ui.sub_pages(
                        {
                            '/settings': self.settings_account, 
                            '/settings/other': self.settings_other,
                            '/settings/projects': self.settings_project,
                            '/settings/users': self.settings_users,
                            '/settings/nyi': self.settings_nyi
                        }
                    ).classes('w-full')

    @ui.refreshable
    def menu(self):
        for k, v in settings_menu.items():
            Heading(k, "xs")
            for item in v:
                menu_item(item['title'], item['link'], icon=item['icon'], is_active=(item['name']==self.active))

    def settings_account(self):
        self.active = 'account'
        self.menu.refresh()
        
        with ui.card().classes("w-full"):
            
            with ui.row().classes('w-full'):
                with ui.column().classes('w-3/7'):
                    ui.label("Name").classes('text-bold')
                    ui.label("Some text")
                with ui.column().classes('w-3/7'):
                    ui.input(value="demo").props('readonly disable')

            ui.separator()
            with ui.row().classes('w-full'):
                with ui.column().classes('w-3/7'):
                    ui.label("Language").classes('text-bold')
                    ui.label("Some text")
                with ui.column().classes('w-3/7'):
                    ui.select(options=['English', 'Dutch'], value="Dutch").props('readonly disable')

        Heading("Subscription", "xs")
        with ui.card().classes("w-full"):
            ui.label("Subscription")

        Heading("Environment", "xs")
        with ui.card().classes("w-full"):
            ui.label("Environment")
            
            

    def settings_other(self):
        self.active = 'other'
        self.menu.refresh()

        with ui.card().classes("w-full"):
            ui.label("Other")


    def settings_project(self):
        self.active = 'projects'
        self.menu.refresh()
        ProjectsManagement()

    def settings_users(self):
        self.active = 'users'
        self.menu.refresh()
        UserManagement()

    def settings_nyi(self):
        with ui.card().classes("w-full"):
            ui.label("NYI")
            self.active = ''
            self.menu.refresh()