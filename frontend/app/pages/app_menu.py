
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
