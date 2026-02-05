from nicegui import ui

from app.client.apps import get_application, set_application
from app.client import APIException


class ApplicationInformation:
    def __init__(self, app_id ) -> None:
        self.current_app = app_id

        self.application = get_application(app_id)

        abbr = ui.label(f"Abbreviation: {self.application['shortname']}")
        name = ui.input("Name").bind_value(self.application, "name").classes("w-full")
        description = ui.textarea("Description").bind_value(self.application, "description").classes("w-full")
        with ui.row().classes("w-full"):
            icon_name = ui.input(
                "Iconname", on_change=lambda: self.ui_app_icon.refresh()
            ).bind_value(self.application, "icon")
            self.ui_app_icon()
            ui.link(text="Material Icons site", target="https://fonts.google.com/icons?icon.set=Material+Icons&icon.style=Filled", new_tab=True)

        ui.button("Save", on_click=self.save_app)

    @ui.refreshable
    def ui_app_icon(self):
        ui.icon(name=self.application['icon']).props('fixed-bottom size="3em"')


    def save_app(self):
        try:
            result = set_application(self.current_app, self.application)
            ui.notify("Success", type="positive")
        except APIException as e:
            ui.notify(f"Fail: {e}", type="negative")
        