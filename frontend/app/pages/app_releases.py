from nicegui import APIRouter
from fastapi import Request

from app.pages.template import frame
from .app_menu import application_menu
from app.components.common import Heading
from app.components.releases import Releases

router = APIRouter(prefix="/app")

@router.page("/{application}/releases")
def application_releases(application, request: Request = None):
    query_params = dict(request.query_params)
    # print(f"QUERY PARAMS: {query_params}")
    with frame(
        f"- Application {application} -", application_menu(application), "releases"
    ):
        Heading("Application Releases")

        Releases(application, query_params)
