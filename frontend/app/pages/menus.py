main_menu = {
    "title": "Menu",
    "items": [
        dict(name="dashboard", text="Dashboard", path="/", icon="dashboard"),
        dict(name="items", text="Items", path="/items", icon="work_outline"),
        dict(
            name="settings",
            text="User settings",
            path="/settings",
            icon="manage_accounts",
        ),
    ],
    "admin": [
        dict(
            name="admin",
            text="Admin",
            path="/admin",
            icon="admin_panel_settings",
            is_admin=True,
        ),
    ],
}
