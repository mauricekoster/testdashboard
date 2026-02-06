from nicegui import ui
from app.client import APIException

from app.client.users import read_user_me


class CurrentUser:
    def __init__(self):
        self.id = 0
        self.email = ""
        self.full_name = ""
        self.is_active = False
        self.is_superuser = False

    def check(self):
        if self.id == 0:
            self.update()

    def update(self):
        try:
            result = read_user_me()
            self.id = result.id
            self.email = result.email
            self.full_name = result.full_name
            self.is_active = result.is_active
            self.is_superuser = result.is_superuser
        except APIException as e:
            ui.notify(e)

    def is_admin(self) -> bool:
        return self.is_superuser
    
current_user = CurrentUser()
