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


text_sizes = {
    "9xl": "8rem",
    "8xl": "6rem",
    "7xl": "4,5rem",
    "6xl": "3.75rem",
    "5xl": "3rem",
    "4xl": "2.25rem",
    "3xl": "1.875rem",
    "2xl": "1.5rem",
    "xl": "1.25rem",
    "lg": "1.125rem",
    "md": "1rem",
    "sm": "0.875rem",
    "xs": "0.75rem",
    "2xs": "0.625rem",
    "3xs": "0.45rem",
}


class Text:
    def __init__(self, text: str, font_size="md"):
        size = text_sizes.get(font_size, font_size)
        self.label = ui.label(text).style(f"font-size: {size};")
