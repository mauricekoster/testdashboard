from nicegui import ui
from contextlib import contextmanager


@contextmanager
def Flex(direction="horizontal"):
    if direction == "horizontal":
        with ui.row():
            yield
    else:
        with ui.column():
            yield
