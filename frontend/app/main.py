#!/usr/bin/env python3
import os
from fastapi import Request
from fastapi.responses import RedirectResponse
from starlette.middleware.base import BaseHTTPMiddleware

from nicegui import Client, app, ui

from . import dashboard
from . import login
from . import projects

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

dashboard.init()
login.init()
projects.init()


# ui.run_with(
#     app,
#     title="Test Dashboard",
#     storage_secret="pick your private secret here",  # NOTE setting a secret is optional but allows for persistent storage per user
# )
#
def handle_shutdown():
    print("Shutdown has been initiated!")


app.on_shutdown(handle_shutdown)
ui.run_with(
    app,
    title="Test Dashboard",
    storage_secret=os.environ.get("STORAGE_SECRET", "very very secret"),
)
print("huh")
