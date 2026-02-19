from fastapi import APIRouter
from fastapi import WebSocket, WebSocketDisconnect
import json
from datetime import datetime
import logging

from .manager import connection_manager


logger = logging.getLogger(__name__)

ws_router = APIRouter()

@ws_router.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await connection_manager.connect(websocket)
    
    logger.info(f"WS: Connected: {client_id}")
    msg = dict(
            event='connect',
            sender=client_id,
            timestamp=datetime.now().isoformat(),
            data=None
        )
    data=json.dumps(msg)
    await connection_manager.broadcast(data)
    try:
        while True:
            data = await websocket.receive_text()
            logger.info(f"WS Broadcast: {data}")
            await connection_manager.broadcast(data)
    except WebSocketDisconnect:
        
        connection_manager.disconnect(websocket)
        logger.info(f"WS: Disconnected: {client_id}")
        msg = dict(
                event='disconnect',
                sender=client_id,
                timestamp=datetime.now().isoformat(),
                data=None
            )
        data=json.dumps(msg)
        await connection_manager.broadcast(data)