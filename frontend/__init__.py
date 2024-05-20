#!/usr/bin/env python3
"""This is just a simple authentication example.

Please see the `OAuth2 example at FastAPI <https://fastapi.tiangolo.com/tutorial/security/simple-oauth2/>`_  or
use the great `Authlib package <https://docs.authlib.org/en/v0.13/client/starlette.html#using-fastapi>`_
to implement a classing real authentication system.
Here we just demonstrate the NiceGUI integration.
"""

from typing import Optional

from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from starlette.middleware.base import BaseHTTPMiddleware

from nicegui import Client, app, ui

from .page_template import mainpage
from . import dashboard, projects

# in reality users passwords would obviously need to be hashed
passwords = {"user1": "pass1", "user2": "pass2"}

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


def init(fastapi_app: FastAPI) -> None:
    app.add_middleware(AuthMiddleware)

    @ui.page("/")
    def show_dashboard():
        with mainpage("Dashboard"):
            dashboard.content()

    @ui.page("/projects")
    def show_projects():
        with mainpage("Projects"):
            projects.content()

    @ui.page("/login")
    def login() -> Optional[RedirectResponse]:
        def try_login() -> (
            None
        ):  # local function to avoid passing username and password as arguments
            if passwords.get(username.value) == password.value:
                app.storage.user.update(
                    {"username": username.value, "authenticated": True}
                )
                ui.navigate.to(
                    app.storage.user.get("referrer_path", "/")
                )  # go back to where the user wanted to go
            else:
                ui.notify("Wrong username or password", color="negative")

        if app.storage.user.get("authenticated", False):
            return RedirectResponse("/")
        with ui.card().classes("absolute-center"):
            username = ui.input("Username").on("keydown.enter", try_login)
            password = ui.input(
                "Password", password=True, password_toggle_button=True
            ).on("keydown.enter", try_login)
            ui.button("Log in", on_click=try_login)
        return None

    ui.run_with(
        fastapi_app,
        mount_path="/",  # NOTE this can be omitted if you want the paths passed to @ui.page to be at the root
        storage_secret="pick your private secret here",  # NOTE setting a secret is optional but allows for persistent storage per user
    )
