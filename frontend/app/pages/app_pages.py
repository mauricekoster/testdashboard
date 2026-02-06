from app.components.common import Heading
from app.pages.template import frame
from app.components import heading

from nicegui import APIRouter, ui

router = APIRouter(prefix="/app")


@router.page("/")
def example_page():
    menu = {"items": [dict(name="home", text="Home", path="/", icon="home")]}
    with frame("- Applications -", menu):
        Heading("Applications")


class AppIcon:
    name: str


app_icon = AppIcon()


@ui.refreshable
def ui_app_icon():
    ui.icon(name=app_icon.name)


@router.page("/add")
def new_app():
    def save_app():
        ui.notify("Save app")
        data = dict(
            app=abbr.value,
            fullname=name.value,
            description=description.value,
            icon=icon_name.value,
        )

    menu = {"items": [dict(name="home", text="Home", path="/", icon="home")]}
    with frame("- New Application -", menu, "add-app"):
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

