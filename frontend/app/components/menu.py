from nicegui import ui
from app.login import current_user


def menu_item(text, target, icon, is_active=False):
    color = "primary" if is_active else "secondary"

    with ui.link(target=target):
        ui.button(text, icon=icon, color=color).style("width: 250px;").props(
            "no-caps flat align='left'"
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
