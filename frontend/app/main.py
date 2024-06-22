#!/usr/bin/env python3
import os
from pathlib import Path


from nicegui import app, ui

from . import login

from .pages import dashboard
from .pages import admin
from .pages import projects
from .pages import items
from .pages import settings

from .middleware import AuthMiddleware


app.add_middleware(AuthMiddleware)

assets_path = Path(__file__).parent / "assets"
app.add_static_files("/assets", assets_path)
# app.add_media_files("/assets", assets_path)

dashboard.init()
admin.init()
login.init()
projects.init()
items.init()
settings.init()


def handle_shutdown():
    print("Shutdown has been initiated!")


app.on_shutdown(handle_shutdown)
ui.run_with(
    app,
    title="Test Dashboard",
    storage_secret=os.environ.get("STORAGE_SECRET", "very very secret"),
)
