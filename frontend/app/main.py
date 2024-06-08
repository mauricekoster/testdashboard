#!/usr/bin/env python3
import os
from pathlib import Path

from fastapi import Request
from fastapi.responses import RedirectResponse
from starlette.middleware.base import BaseHTTPMiddleware

from nicegui import Client, app, ui

from . import dashboard
from . import admin
from . import login
from . import projects
from . import items
from . import settings

unrestricted_page_routes = {"/login"}


class AuthMiddleware(BaseHTTPMiddleware):
    """This middleware restricts access to all NiceGUI pages.

    It redirects the user to the login page if they are not authenticated.
    """

    async def dispatch(self, request: Request, call_next):
        if not app.storage.user.get("authenticated", False):
            if (
                request.url.path in Client.page_routes.values()
                and request.url.path not in unrestricted_page_routes
            ):
                app.storage.user["referrer_path"] = (
                    request.url.path
                )  # remember where the user wanted to go
                return RedirectResponse("/login")
        return await call_next(request)


app.add_middleware(AuthMiddleware)

assets_path = Path(__file__).parent / "assets"
app.add_media_files("/assets", assets_path)

dashboard.init()
admin.init()
login.init()
projects.init()
items.init()
settings.init()


def handle_shutdown():
    print("Shutdown has been initiated!")


app.on_shutdown(handle_shutdown)
ui.run_with(
    app,
    title="Test Dashboard",
    storage_secret=os.environ.get("STORAGE_SECRET", "very very secret"),
)
