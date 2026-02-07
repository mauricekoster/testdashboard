from nicegui import APIRouter
from fastapi import Request

from .menus import application_menu
from app.pages.templates.detail import detailpage
from app.components.common import Heading
from app.components.resultsdashboard import ResultsDashboard

router = APIRouter(prefix="/app")

@router.page("/{app_id}")
def application_dashboard(app_id: str, request: Request = None):
    query_params = dict(request.query_params)
    with detailpage("resultsdashboard", application_menu(app_id), "dashboard"):
        Heading("Dashboard")
        ResultsDashboard(app_id, query_params)



