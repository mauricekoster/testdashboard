from contextlib import contextmanager
from nicegui import ui


async def alert_dialog(title: str, message: str, action: str = "Delete"):
    with ui.dialog() as dialog, ui.card().style("width: 50%;"):
        with ui.card_section().classes("w-full"):
            with ui.row():
                ui.label(title).classes("text-h6")
                ui.space()
                ui.button(
                    icon="close",
                    on_click=lambda: dialog.submit("Cancel"),
                ).props("round flat dense")

        with ui.card_section().classes("w-full"):
            with ui.row().classes("w-full"):
                ui.label(message)

        with ui.card_actions().classes("w-full").props("align=right"):
            ui.button(action, color="red", on_click=lambda: dialog.submit(action))
            ui.button(
                "Cancel",
                color="secondary",
                on_click=lambda: dialog.submit("Cancel"),
            )

    answer = await dialog
    return answer


async def user_dialog(title: str, data):
    with ui.dialog() as user_dialog, ui.card().style("width: 50%;"):
        with ui.card_section().classes("w-full"):
            with ui.row():
                ui.label(title).classes("text-h6")
                ui.space()
                ui.button(
                    icon="close",
                    on_click=lambda: user_dialog.submit("Cancel"),
                ).props("round flat dense")

        with ui.card_section().classes("w-full"):
            ui.input("Email").bind_value(data, "email")
            ui.input("Full name").bind_value(data, "full_name")
            set_password = ui.input("Set password", password=True).bind_value(
                data, "password"
            )
            ui.input(
                "Confirm password",
                password=True,
                validation={
                    "Password not same": lambda value: value == set_password.value
                },
            )
            with ui.row().classes("w-full"):
                ui.checkbox("Is superuser?").bind_value(data, "is_superuser")
                ui.checkbox("Is active?", value=True).bind_value(data, "is_active")

        with ui.card_actions().classes("w-full").props("align=right"):
            ui.button("Save", on_click=lambda: user_dialog.submit("Save"))
            ui.button(
                "Cancel",
                color="secondary",
                on_click=lambda: user_dialog.submit("Cancel"),
            )

    answer = await user_dialog
    return answer
