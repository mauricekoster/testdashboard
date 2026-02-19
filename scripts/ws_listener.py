#!/usr/bin/env python

import asyncio
import signal

from websockets.asyncio.client import connect

async def client(client_id):
    async with connect(f"ws://localhost:8000/ws/{client_id}") as websocket:
        # Close the connection when receiving SIGTERM.
        loop = asyncio.get_running_loop()
        def close():
            return loop.create_task(websocket.close())
        loop.add_signal_handler(signal.SIGTERM, close)

        # Process messages received on the connection.
        async for message in websocket:
            print(message)

asyncio.run(client(1234))