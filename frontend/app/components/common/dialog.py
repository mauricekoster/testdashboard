from nicegui import ui
from typing_extensions import Callable
from functools import partial


class Dialog:
    def __init__(self, title, content: Callable | None = None, buttons=[]):
        self.title = title
        self.buttons = buttons
        self.content = content
        self._callbacks = {}

        for name, _, callback in self.buttons:
            self._callbacks[name] = callback

        with ui.dialog() as self._dialog, ui.card().style("width: 50%;"):
            with ui.card_section().classes("w-full"):
                with ui.row():
                    ui.label(self.title).classes("text-h6")
                    ui.space()
                    ui.button(
                        icon="close",
                        on_click=lambda: self._dialog.submit("Cancel"),
                    ).props("round flat dense")

            with ui.card_section().classes("w-full"):
                if self.content:
                    self.content()
                else:
                    ui.label("NO CONTENT")

            with ui.card_actions().classes("w-full").props("align=right"):
                for name, color, _ in self.buttons:
                    ui.button(
                        name, color=color, on_click=partial(self._dialog.submit, name)
                    )


    async def _handle_submit(self):
        pass

    async def show(self):
        answer = await self._dialog
        print(f"ANSWER: {answer}")
        callback = self._callbacks.get(answer, None)
        if callback:
            callback()
