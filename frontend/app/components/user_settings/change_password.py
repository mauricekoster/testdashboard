from nicegui import ui
from app.components.common import Heading, Input, Form, FormLabel


class ChangePassword:
    def __init__(self):
        Heading("Change password", size="sm")

        with Form(self, on_submit=self.handle_submit) as form:
            FormLabel("Current Password")
            Input(form, "current_password", placeholder="Password", type="password")

            FormLabel("Set Password", id="aap")
            Input(form, "set_password", placeholder="Password", type="password")

            FormLabel("Confirm Password")
            Input(form, "confirm_password", placeholder="Password", type="password")

            ui.button("Save", on_click=form.submit)

    def handle_submit(self, data):
        ui.notify(f"Save! {data}")
