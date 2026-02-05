from nicegui import APIRouter
from fastapi import Request

from .app_menu import application_menu
from app.pages.template import frame
from app.components.common import Heading
from app.components.dashboard import Dashboard

router = APIRouter(prefix="/app")

@router.page("/{app_id}")
def application_dashboard(app_id: str, request: Request = None):
    query_params = dict(request.query_params)
    with frame(f"- Application {app_id} -", application_menu(app_id), "dashboard"):
        Heading("Dashboard")
        Dashboard(app_id, query_params)



