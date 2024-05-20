from nicegui import ui

columns = [
    {
        "name": "name",
        "label": "Name",
        "field": "name",
        "required": True,
        "align": "left",
    },
    {"name": "latest", "label": "Latest", "field": "latest", "sortable": True},
    {"name": "current", "label": "Current", "field": "current", "sortable": True},
]
rows = [
    {"name": "First project", "latest": "FAIL", "current": "PASS"},
]


def content() -> None:
    ui.label("Projects here...")
    ui.table(columns=columns, rows=rows, row_key="name")
    ui.label("Latest: latest results. Current: results from current release.")
