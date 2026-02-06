from dataclasses import dataclass

from app.components.common import Heading
from app.pages.template import mainpage
from app.components import heading
from app.client.apps import set_application
from app.models import ApplicationInfo

from nicegui import APIRouter, ui

router = APIRouter(prefix="/app")


@router.page("/")
def example_page():
    menu = {"items": [dict(name="home", text="Home", path="/", icon="home")]}
    with mainpage("- Applications -", menu):
        Heading("Applications")

@dataclass
class AppIcon:
    name: str
    


app_icon = AppIcon(None)


@ui.refreshable
def ui_app_icon():
    ui.icon(name=app_icon.name)


@router.page("/add")
def new_app():
    def save_app():
        ui.notify("Save app")
        data = ApplicationInfo(
            shortname=abbr.value,
            name=name.value,
            description=description.value,
            icon=icon_name.value,
        )
        set_application(abbr.value, data)

    menu = {"items": [dict(name="home", text="Home", path="/", icon="home")]}
    with mainpage("- New Application -", menu, "add-app"):
        heading("Add application", 4)
        abbr = ui.input("Abbreviation (e.g. XYZ)")
        name = ui.input("Name").classes("w-full")
        description = ui.textarea("Description").classes("w-full")
        with ui.row().classes("w-full"):
            icon_name = ui.input(
                "Iconname", on_change=lambda: ui_app_icon.refresh()
            ).bind_value(app_icon, "name")
            ui_app_icon()

        ui.button("Save", on_click=save_app)

