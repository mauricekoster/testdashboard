from nicegui import ui

class Icon:
    def __init__(self, icon_name: str, size="md", color: str = "blue-3"):
        self.icon = ui.icon(icon_name).classes(f'rounded bg-{color} text-white text-{size}')
        

