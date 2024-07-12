from nicegui import ui

heading_sizes = {
    "2xl": "h1",
    "xl": "h2",
    "lg": "h3",
    "md": "h4",
    "sm": "h5",
    "xs": "h6",
}


class Heading:
    def __init__(self, text: str, size: str = "md", font_size: str | None = None):
        level = heading_sizes.get(size, "h4")
        self.label = ui.label(text).classes(f"text-{level}")
        if font_size:
            self.label.style(add=f"font-size: {font_size};")
