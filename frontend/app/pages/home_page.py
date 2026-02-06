from app.components.message import message

from nicegui import ui, APIRouter
from app.pages.template import mainpage
from app.client.apps import get_apps
from pprint import pprint

router = APIRouter()


def make_menu(title):
    d = {}
    items = []
    apps = get_apps()
    pprint(apps)
    for app in apps:
        if isinstance(app, str):
            items.append(
                dict(name=app, text=app, path=f"/app/{app}", icon="assignment")
            )
        else:
            short_name = app.get("shortname", app.get("name", "UNKNOWN"))
            items.append(
                dict(
                    name=short_name,
                    text=app.get("name", "UNKNOWN"),
                    path=f"/app/{short_name}",
                    icon=app.get("icon", "work"),
                )
            )

    d["title"] = title
    d["items"] = items
    d["admin"] = [
        dict(name="add-app", text="Add application", path="/app/add", icon="add_box")
    ]
    return d


@router.page("/home")
def index_page() -> None:
    menu = make_menu("Applications")
    with mainpage("Homepage", menu, "homepage"):
        content()


def content() -> None:
    message("This is the home page.").classes("font-bold")
    ui.label("Use the menu on the left side to navigate.")
