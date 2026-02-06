from nicegui import APIRouter, ui

from .templates.landing import landingpage

from app.components.common import Heading

router = APIRouter()

@router.page("/settings")
def show_dashboard():
    
    with landingpage("settings"):
        
        with ui.row().classes("w-full"):
            Heading("Settings")
        ui.separator()

        with ui.row().classes("flex w-full"):
            with ui.column().classes("flex w-1/3"):
                Heading("General", "sm")
                Heading("Projects & Tests", "sm")

            with ui.column().classes("flex w-3/5"):
                with ui.card().classes("w-full"):
                    ui.label("Hoi")
        
