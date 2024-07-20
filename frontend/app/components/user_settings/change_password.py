from nicegui import ui
from app.components.common import Heading, Input, Form, FormLabel
from app.client.mutation import Mutation
from app.models import UpdatePassword
from app.client.users import update_password_me
from functools import partial


from app.core.utils.validations import confirm_password_rules


class UpdatePasswordForm(UpdatePassword):
    confirm_password: str


class ChangePassword:
    def __init__(self):
        self.model = UpdatePasswordForm(
            current_password="", new_password="", confirm_password=""
        )
        self.mutation = Mutation(
            mutation_fn=lambda data: update_password_me(data),
            on_success=lambda: ui.notify("Success", type="positive"),
            on_error=lambda err: ui.notify(
                f"Something went wrong! {err.detail}", type="negative"
            ),
        )

        Heading("Change password", size="sm")

        with Form(self.model, on_submit=self.handle_submit) as form:
            FormLabel("Current Password")
            Input(form, id="current_password", placeholder="Password", type="password")

            FormLabel("Set Password", id="aap")
            Input(
                form,
                id="new_password",
                placeholder="Password",
                type="password",
                validation={"Too short": lambda value: len(value) >= 5},
            )

            FormLabel("Confirm Password")
            Input(
                form,
                id="confirm_password",
                placeholder="Password",
                type="password",
                validation={
                    "The passwords do not match": partial(
                        confirm_password_rules, form.get_values
                    )
                },
            )

            ui.button("Save", on_click=form.submit)

    def handle_submit(self, data):
        print(data)
        print(self.model)
        pwd = UpdatePassword(
            current_password=self.model.current_password,
            new_password=self.model.confirm_password,
        )
        self.mutation(pwd)
