from nicegui import ui
from contextlib import contextmanager


@contextmanager
def navbar():
    with ui.card().classes("w-full").tight():
        with ui.card_actions():
            yield
