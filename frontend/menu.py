from nicegui import ui


def main_menu() -> None:
    ui.link("Dashboard", "/").classes(replace="text-black")
    ui.link("Projects", "/projects").classes(replace="text-black")
