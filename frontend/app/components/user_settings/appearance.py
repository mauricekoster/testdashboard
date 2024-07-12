from nicegui import ui, app
from app.components.common import Heading


class Appearance:
    def __init__(self):
        Heading("Appearance", size="sm")
        ui.switch("Darkmode").bind_value(app.storage.user, "dark_mode").props("flat")
