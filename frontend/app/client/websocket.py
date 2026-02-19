from websockets.asyncio.client import connect
import asyncio
import signal
from nicegui import Event
from app.core.config import settings
import logging
import json


logger = logging.getLogger(__name__)


class Connection():

    def __init__(self):
        self.user_id = None
        self.event = None
        self.events = {}
        self.websocket = None

        self.base_url = settings.BACKEND_WS_URL
        if settings.WS_STR:
            self.base_url = f"{settings.BACKEND_WS_URL}{settings.WS_STR}"

    def set_default_handler(self, callback):
        self.events['*DEFAULT*'] = Event()
        self.events['*DEFAULT*'].subscribe(callback)

    def on(self, event, callback):
        self.events[event] = Event()
        self.events[event].subscribe(callback)

    async def start_task(self, user_id):
        # self.user_id = user_id
        logger.info(f"WS Connect base URL: {self.base_url}. userid={user_id}")
        async with connect(f"{self.base_url}/{user_id}") as websocket:
            # Close the connection when receiving SIGTERM.
            loop = asyncio.get_running_loop()
            def close():
                return loop.create_task(websocket.close())
            loop.add_signal_handler(signal.SIGTERM, close)

            self.websocket = websocket

            # Process messages received on the connection.
            async for message in websocket:
                if self.event:
                    event = None
                    if message[0] == '{' and message[-1] == '}':
                        
                        # assume json object
                        data = json.loads(message)
                        event = data['event']
                        logger.info(f"WS Got JSON: ({event}) {data}")
                    else:
                        logger.info(f"WS Got Plain: {message}")
                        event = '*DEFAULT*'
                        data = message

                    if event in self.events:
                        self.events[event].emit(data)
            
    async def send_text(self, message):
        await self.websocket.send(message, text=True)

    async def send_json(self, data):
        """
        data: a python object, will be serialized as JSON
        """
        logger.info("WS Sending json data")
        msg = json.dumps(data, separators=(",", ":"), ensure_ascii=False)
        await self.websocket.send(msg, text=True)

connection = Connection()
