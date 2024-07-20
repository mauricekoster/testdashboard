from nicegui import ui
from app.client.mutation import Mutation
from app.client.users import delete_user_me
from app.components.common import Heading, Text
from app.components.user_settings import DeleteConfirmation
from app.pages.login import logout


class DeleteAccount:
    def __init__(self):
        Heading("Delete account", size="sm")

        Text(
            "Permanently delete your data and everything associated with your account."
        )

        ui.button("Delete", color="red", on_click=self._handle_delete)

        self.confirmation = DeleteConfirmation(on_confirm=self.on_confirm)

    async def _handle_delete(self):
        await self.confirmation.show()

    def on_confirm(self):
        def on_success():
            ui.notify("Success")
            logout()
            ui.navigate.to("/")

        def on_error(err):
            ui.notify(f"Something went wrong. {err.detail}")

        Mutation(
            mutation_fn=lambda: delete_user_me(),
            on_success=on_success,
            on_error=on_error,
        )()
