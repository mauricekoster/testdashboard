from libgravatar import Gravatar as RealGravatar
from nicegui import ui
import logging
from contextlib import contextmanager

logger = logging.getLogger(__name__)


class Gravatar():
    def __init__(self, email):
        g = RealGravatar(email)
        image_url = g.get_image(default='retro')
        logger.info(f"Gravatar url: {image_url}")
        with ui.avatar():
            ui.image(image_url)