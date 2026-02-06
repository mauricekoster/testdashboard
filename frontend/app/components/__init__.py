from nicegui import ui


def menu_item(text, target, icon, is_active=False):
    color = "primary" if is_active else "secondary"

    with ui.link(target=target):
        ui.button(text, icon=icon, color=color).style("width: 250px;").props(
            "no-caps flat align='left'"
        )


def heading(title, level=1):
    ui.label(title).classes(f"text-h{level}").style("padding-top: 12px")
