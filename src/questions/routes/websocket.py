from typing import List, Optional, Union

from fastapi import WebSocket, WebSocketDisconnect
from base.database import engine, Base, get_db
from auth.backend import authenticate_via_websockets
from auth import schemas as auth_schemas
from questions.schemas import polls as polls_shcemas
from questions.models import Poll, Vote


Base.metadata.create_all(bind=engine)


class Room():
    def __init__(self, room_id: int) -> None:
        self.room_id = room_id
        self.active_connections: List[WebSocket] = []

    async def connect(self, webosocket: WebSocket):
        await webosocket.accept()
        self.active_connections.append(webosocket)

    async def broadcast(self, data: dict):
        for connection in self.active_connections:
            await connection.send_json(data)

    async def send_personal_message(self, data: dict, websocket: WebSocket):
        await websocket.send_json(data)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.rooms: List[Room] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    async def connect_to_room(self, websocket: WebSocket, room_id: int):
        connected = False
        for room in self.rooms:
            if room_id == room.room_id:
                connected = True
                await room.connect(websocket)

        if not connected:
            room = Room(room_id=room_id)
            await room.connect(websocket)
            self.rooms.append(room)
        self.active_connections.append(websocket)

    def get_room(self, room_id: int) -> Union[Room, None]:
        for room in self.rooms:
            if room_id == room.room_id:
                return room

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    def disconnect_from_room(self, room_id: int, websocket: WebSocket):
        room = self.get_room(room_id)
        room.active_connections.remove(websocket)

    async def send_personal_message(self, data: dict, websocket: WebSocket):
        await websocket.send_json(data)

    async def send_personal_message_to_room(
        self,
        room_id: int,
        data: dict,
        websocket: WebSocket
    ):
        room = self.get_room(room_id)
        print(room)
        await room.send_personal_message(data, websocket)

    async def broadcast(self, data: dict):
        for connection in self.active_connections:
            await connection.send_json(data)

    async def broadcast_to_room(self, room_id: int, data: dict) -> None:
        room = self.get_room(room_id)
        await room.broadcast(data)


manager = ConnectionManager()
