from nicegui import ui
from contextlib import contextmanager


def heading(title, level=1):
    ui.label(title).classes(f"text-h{level}").style("padding-top: 12px")


@contextmanager
def navbar():
    with ui.card().classes("w-full").tight():
        with ui.card_actions():
            yield
