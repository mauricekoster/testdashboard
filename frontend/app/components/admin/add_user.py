from app.components.common import Dialog
from app.components.common import Form, Input, FormLabel, Flex
from functools import partial
from app.components.common.form import Checkbox

from app.client.mutation import Mutation
from app.client.users import create_user

from nicegui import ui

from app.models import UserCreate


def confirm_password_rules(get_values, value):
    values = get_values()
    return values["password"] == values["confirm_password"]


class AddUser:
    def __init__(self, userlist):
        self.userlist = userlist
        self.model = {
            "email": "",
            "full_name": "",
            "password": "",
            "confirm_password": "",
            "is_superuser": False,
            "is_active": True,
        }

    def content(self):
        with Form(self.model) as form:
            Input(form, "email", "Email adres")
            Input(form, "full_name", "Full name")
            Input(
                form,
                id="password",
                placeholder="Set password",
                type="password",
                validation={"Too short": lambda value: len(value) >= 5},
            )
            Input(
                form,
                id="confirm_password",
                placeholder="Confirm password",
                type="password",
                validation={
                    "The passwords do not match": partial(
                        confirm_password_rules, form.get_values
                    )
                },
            )

            with Flex():
                Checkbox(form, "is_superuser", "Is superuser?")
                Checkbox(form, "is_active", "Is active?")

    async def show(self):
        dialog = Dialog(
            "Add user",
            content=self.content,
            buttons=[
                ("Save", "primary", self._handle_confirm),
                ("Cancel", "secondary", self._handle_cancel),
            ],
        )
        await dialog.show()

    def _handle_confirm(self):
        data = UserCreate.model_validate(self.model)
        Mutation(
            mutation_fn=lambda data: create_user(data),
            on_success=lambda: self.userlist.refresh(),
            on_error=lambda err: ui.notify(
                f"Something went wrong: {err.detail}", type="negative"
            ),
        )(data)

    def _handle_cancel(self):
        pass
