from typing import Optional
from fastapi.responses import RedirectResponse
from nicegui import ui, app, APIRouter
from app.client import APIException
from app.client.login import login_access_token

from app.core.user import current_user

router = APIRouter()


@router.page("/login")
def login() -> Optional[RedirectResponse]:
    def try_login() -> (
        None
    ):  # local function to avoid passing username and password as arguments
        try:
            token = login_access_token(username.value, password.value)

            app.storage.user.update(
                {
                    "username": username.value,
                    "authenticated": True,
                    "access_token": token.access_token,
                }
            )
            current_user.update()
            print(current_user)

            ui.navigate.to(
                #app.storage.user.get("referrer_path", "/")
                "/projects"
            )  # go back to where the user wanted to go
        except APIException as e:
            ui.notify(e, color="negative")

    if app.storage.user.get("authenticated", False):
        return RedirectResponse("/")

    with ui.card().classes("absolute-center"):
        ui.image("/assets/fastapi-logo.svg")
        username = ui.input("Email").on("keydown.enter", try_login)
        password = ui.input("Password", password=True, password_toggle_button=True).on(
            "keydown.enter", try_login
        )
        ui.button("Log in", on_click=try_login).classes("w-full")
    return None


@router.page("/logout")
def logout() -> Optional[RedirectResponse]:
    app.storage.user.update(
        {
            "username": "",
            "authenticated": False,
            "access_token": "",
        }
    )
    return RedirectResponse("/login")
