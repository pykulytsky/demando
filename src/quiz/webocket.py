from dataclasses import dataclass
from typing import List, Union

from fastapi import WebSocket
from sqlalchemy.orm import Session

from auth.backend import authenticate_via_websockets
from auth.models import User
from core.database import Base, engine
from questions.routes.websocket import ConnectionManager, Room

Base.metadata.create_all(bind=engine)


@dataclass()
class Connection:
    websocket: WebSocket
    member: User


class QuizRoom(Room):
    def __init__(self, enter_code: str) -> None:
        self.enter_code = enter_code
        self.active_connections: List[Connection] = []

    async def connect(self, webosocket: WebSocket, member: User):
        await webosocket.accept()
        self.active_connections.append(Connection(webosocket, member))

    def disconnect(self, websocket: WebSocket):
        for connection in self.active_connections:
            if connection.websocket == websocket:
                self.active_connections.remove(connection)


class QuizConnectionManager(ConnectionManager):
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.rooms: List[QuizRoom] = []

    async def connect_to_room(
        self, websocket: WebSocket, enter_code: str, token: str, db: Session
    ):
        member = authenticate_via_websockets(token, db)
        connected = False
        for room in self.rooms:
            if enter_code == room.enter_code:
                connected = True
                await room.connect(websocket, member)

        if not connected:
            room = QuizRoom(enter_code=enter_code)
            await room.connect(websocket, member)
            self.rooms.append(room)
        self.active_connections.append(websocket)

    def get_room(self, enter_code: str) -> Union[Room, None]:
        for room in self.rooms:
            if enter_code == room.enter_code:
                return room

    def disconnect_from_room(self, enter_code: str, websocket: WebSocket):
        room = self.get_room(enter_code)
        room.disconnect(websocket)

    async def send_personal_message_to_room(
        self, enter_code: str, data: dict, websocket: WebSocket
    ):
        room = self.get_room(enter_code)
        await room.send_personal_message(data, websocket)

    async def broadcast_to_room(self, enter_code: str, data: dict) -> None:
        room = self.get_room(enter_code)
        await room.broadcast(data)


quiz_manager = QuizConnectionManager()
