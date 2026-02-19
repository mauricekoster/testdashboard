from nicegui import ui, app
from app.core.user import current_user


def menu_item(text, target, icon, is_active=False):
    color = "primary" if is_active else "secondary"
    border = "border" if is_active else ""

    with ui.link(target=target):
        ui.button(text, icon=icon, color=color).style("width: 250px;").props(
            f"no-caps {border} outline rounded align='left'"
        )


def display_menu(menu_definition, active_menu="") -> None:
    if "title" in menu_definition:
        ui.label(menu_definition["title"]).classes("text-h6")

    for m in menu_definition["items"]:
        is_active = m["name"] == active_menu
        menu_item(m["text"], m["path"], m["icon"], is_active)

    if "admin" in menu_definition:
        if current_user.is_superuser:
            ui.space()
            for m in menu_definition["admin"]:
                is_active = m["name"] == active_menu
                menu_item(m["text"], m["path"], m["icon"], is_active)


def UserDropdownMenu():

    with ui.dropdown_button(
            icon="account_circle", auto_close=True
        ).props("rounded no-caps").classes("q-ma-sm"):
            with ui.row().classes("m-3"):
                ui.label(f"Signed in as:").classes("text")
                ui.label(current_user.full_name).classes("text-bold")
            ui.separator()
            ui.item("My account...", on_click=lambda: ui.navigate.to("/myprofile"))
            ui.item("My work...", on_click=lambda: ui.navigate.to("/mywork"))
            ui.separator()
            ui.item("Log out", on_click=lambda: ui.navigate.to("/logout"))
            