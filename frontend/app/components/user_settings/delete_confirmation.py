from app.components.common import Dialog

from nicegui import ui


class DeleteConfirmation:
    def __init__(self, on_confirm=None, on_cancel=None):
        self.on_confirm = on_confirm
        self.on_cancel = on_cancel

    def content(self):
        ui.label("test")
        ui.markdown("""
              All your account data will be **permanently deleted.** If you are sure, please
              click **"Confirm"** to proceed. This action cannot be undone.
                    """)

    async def show(self):
        dialog = Dialog(
            "Confirmation Required",
            content=self.content,
            buttons=[
                ("Confirm", "red", self._handle_confirm),
                ("Cancel", "grey", self._handle_cancel),
            ],
        )
        await dialog.show()

    def _handle_confirm(self):
        if self.on_confirm:
            self.on_confirm()

    def _handle_cancel(self):
        if self.on_cancel:
            self.on_cancel()
