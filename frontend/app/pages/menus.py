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


def application_menu(app_id):
    return {
        "title": app_id,
        "items": [
            dict(name="home", text="Home", path="/", icon="home"),
            dict(
                name="dashboard",
                text="Dashboard",
                path=f"/app/{app_id}",
                icon="dashboard",
            ),
            dict(
                name="releases",
                text="Releases",
                path=f"/app/{app_id}/releases",
                icon="new_releases",
            ),
        ],
        "admin": [
            dict(name="app-settings", text="Settings", path=f"/app/{app_id}/settings", icon="settings")
        ]
    }
