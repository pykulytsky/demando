from typing import List

from fastapi import WebSocket, WebSocketDisconnect
from base.database import engine, Base, get_db
from auth.backend import authenticate_via_websockets
from auth import schemas as auth_schemas
from questions.schemas import polls as polls_shcemas
from questions.models import Poll


Base.metadata.create_all(bind=engine)


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, data: dict, websocket: WebSocket):
        await websocket.send_json(data)

    async def broadcast(self, data: dict):
        for connection in self.active_connections:
            await connection.send_json(data)


manager = ConnectionManager()


async def vote_websocket(
    websocket: WebSocket,
    poll_id: str,
):
    await manager.connect(websocket)
    db = next(get_db())
    try:
        while True:
            data = await websocket.receive_json()
            user = authenticate_via_websockets(data['token'], db)
            await manager.send_personal_message(
                auth_schemas.User(**user.__dict__).dict(), websocket
            )
            await manager.broadcast(
                polls_shcemas.Poll(
                    **Poll.manager(db).get(pk=poll_id).__dict__
                ).dict()
            )
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast("Client left the chat")
