#!/usr/bin/env python3
import os
from pathlib import Path

from nicegui import app, ui

from .pages import router

from app.core.middleware import AuthMiddleware
from app.core.config import settings

import logging

log = logging.getLogger('main')
logging.basicConfig(level=logging.INFO)

app.include_router(router)
app.add_middleware(AuthMiddleware)

assets_path = Path(__file__).parent / "assets"
app.add_static_files("/assets", assets_path)
# app.add_media_files("/assets", assets_path)
log.info(f"Assets path: {assets_path}")

def handle_shutdown():
    print("Shutdown has been initiated!")


app.on_shutdown(handle_shutdown)
ui.run_with(
    app,
    title=settings.PROJECT_NAME,
    storage_secret=settings.STORAGE_SECRET,
)
