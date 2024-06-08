from typing import Optional
from fastapi.responses import RedirectResponse
from nicegui import ui, app
from .client.main import set_token
from .client.login import login_access_token
from .client.users import read_user_me


class CurrentUser:
    def __init__(self):
        self.id = 0
        self.email = ""
        self.full_name = ""
        self.is_active = False
        self.is_superuser = False

    def update(self, data):
        self.id = data.get("id", 0)
        self.email = data.get("email", None)
        self.full_name = data.get("full_name", None)
        self.is_active = data.get("is_active", False)
        self.is_superuser = data.get("is_superuser", False)


current_user = CurrentUser()


def check_username_password(username, password):
    status, result = login_access_token(username, password)
    print(f"Status: {status}  Result: {result}")
    return status, result


def update_current_user():
    global current_user
    status, result = read_user_me()
    if status:
        current_user.update(result)
    else:
        ui.notify(result)


def init() -> None:
    @ui.page("/login")
    def login() -> Optional[RedirectResponse]:
        def try_login() -> (
            None
        ):  # local function to avoid passing username and password as arguments
            status, result = check_username_password(username.value, password.value)
            if status:
                set_token(result)
                app.storage.user.update(
                    {
                        "username": username.value,
                        "authenticated": True,
                        "access_token": result,
                    }
                )
                update_current_user()
                print(current_user)

                ui.navigate.to(
                    app.storage.user.get("referrer_path", "/")
                )  # go back to where the user wanted to go
            else:
                ui.notify(result, color="negative")

        if app.storage.user.get("authenticated", False):
            return RedirectResponse("/")

        with ui.card().classes("absolute-center"):
            ui.image("/assets/fastapi-logo.svg")
            username = ui.input("Email").on("keydown.enter", try_login)
            password = ui.input(
                "Password", password=True, password_toggle_button=True
            ).on("keydown.enter", try_login)
            ui.button("Log in", on_click=try_login).classes("w-full")
        return None

    @ui.page("/logout")
    def logout() -> Optional[RedirectResponse]:
        app.storage.user.update(
            {
                "username": "",
                "authenticated": False,
                "access_token": "",
            }
        )
        return RedirectResponse("/login")
