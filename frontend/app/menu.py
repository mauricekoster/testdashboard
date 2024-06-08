from nicegui import ui
from .login import current_user

main_menu_options = [
    dict(
        name="admin",
        text="Admin",
        path="/admin",
        icon="admin_panel_settings",
        is_admin=True,
    ),
    dict(name="dashboard", text="Dashboard", path="/", icon="dashboard"),
    dict(name="items", text="Items", path="/items", icon="work_outline"),
    dict(
        name="settings", text="User settings", path="/settings", icon="manage_accounts"
    ),
]


def menu_item(text, target, icon, is_active=False):
    color = "primary" if is_active else "secondary"

    with ui.link(target=target):
        ui.button(text, icon=icon, color=color).style("width: 250px;").props(
            "no-caps outline align='left'"
        )


def menu(menu=main_menu_options, active_menu="") -> None:
    for m in menu:
        is_active = m["name"] == active_menu
        is_admin = "is_admin" in m and m["is_admin"]
        if is_admin and current_user.is_superuser:
            menu_item(m["text"], m["path"], m["icon"], is_active)
        else:
            menu_item(m["text"], m["path"], m["icon"], is_active)
