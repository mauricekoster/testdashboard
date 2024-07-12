from nicegui import ui
from app import components
from app.components.common import Flex, Heading
from app.client.users import read_user_me, update_user_me
from app.models import UserUpdateMe


@ui.refreshable
def user_form(component):
    ui.label("Full name:").classes("text-bold")
    if component.edit_mode:
        ui.input(placeholder="Full name").bind_value(component, "full_name")
    else:
        ui.label().bind_text(component, "full_name")

    ui.label("Email:").classes("text-bold")
    if component.edit_mode:
        ui.input(placeholder="Email").bind_value(component, "email")
    else:
        ui.label().bind_text(component, "email")

    with Flex():
        if component.edit_mode:
            ui.button("Save", on_click=component.save)
            ui.button("Cancel", color="secondary", on_click=component.cancel)
        else:
            ui.button("Edit", on_click=component.edit)


class UserInformation:
    def __init__(self):
        self.edit_mode = False

        userme = read_user_me()

        self.full_name = userme.full_name or "N/A"
        self.email = userme.email

        Heading("User information", size="sm")
        user_form(self)

    def hello(self):
        ui.notify("Hello!")

    def save(self):
        ui.notify("Save!")

        data = UserUpdateMe(full_name=self.full_name, email=self.email)
        try:
            update_user_me(data)
        finally:
            ui.notify("User saved!", type="positive")
            self.edit_mode = False
            user_form.refresh()

    def edit(self):
        self.full_name_orig = self.full_name
        self.email_orig = self.email

        ui.notify("Edit!")
        self.edit_mode = True
        user_form.refresh()

    def cancel(self):
        self.full_name = self.full_name_orig
        self.email = self.email_orig
        ui.notify("Cancelled!")
        self.edit_mode = False
        user_form.refresh()
