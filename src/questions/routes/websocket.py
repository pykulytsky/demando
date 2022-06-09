from datetime import datetime
from typing import List, Union

from fastapi import WebSocket, WebSocketDisconnect
from logger import http_logger

from core.database import Base, engine

Base.metadata.create_all(bind=engine)


class Room:
    def __init__(self, room_id: int) -> None:
        self.room_id = room_id
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    async def broadcast(self, data: dict):
        print(self.active_connections)
        for connection in self.active_connections:
            await self.send_personal_message(data, connection)

    async def send_personal_message(self, data: dict, websocket: WebSocket):
        await http_logger.websocket_info(
            websocket,
            extra_data={
                "connections": len(self.active_connections),
                "websocket": websocket,
                "status": "SENDED",
                "poll": data["pk"]
            }
        )
        await websocket.send_json(data)

    async def disconnect(self, websocket: WebSocket):

        self.active_connections.remove(websocket)

        await http_logger.websocket_info(
            websocket,
            extra_data={
                "connections": len(self.active_connections),
                "websocket": websocket,
                "status": "DISCONNECTED"
            }
        )


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.rooms: List[Room] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    async def connect_to_room(self, websocket: WebSocket, room_id: int):
        print(f"{self.rooms=}")
        connected = False
        already_connected = False
        for room in self.rooms:
            print(f"{room.room_id=}, {room.active_connections=}")
            if room_id == room.room_id:
                # connected = True
                # await room.connect(websocket)
                await http_logger.websocket_info(
                    websocket,
                    extra_data={
                        "connections": len(self.active_connections),
                        "status": "CONNECTED TO EXISTED ROOM",
                        "websocket": websocket
                    }
                )
                # for conn in room.active_connections:
                #     if conn == websocket:
                #         already_connected = True
                #         raise WebSocketDisconnect()

                # if not already_connected:
                connected = True
                await room.connect(websocket)

                print(room.active_connections)

        if not connected:
            print("Created new room")
            room = Room(room_id=room_id)
            await room.connect(websocket)
            self.rooms.append(room)
            await http_logger.websocket_info(
                websocket,
                extra_data={
                    "connections": len(self.active_connections),
                    "status": "CREATED NEW ROOM",
                    "websocket": websocket
                }
            )
            print(room.active_connections)

    def get_room(self, room_id: int) -> Union[Room, None]:
        for room in self.rooms:
            if room_id == room.room_id:
                return room

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def disconnect_from_room(self, room_id: int, websocket: WebSocket):
        room = self.get_room(room_id)
        await room.disconnect(websocket)

    async def send_personal_message(self, data: dict, websocket: WebSocket):
        await websocket.send_json(data)

    async def send_personal_message_to_room(
        self, room_id: int, data: dict, websocket: WebSocket
    ):
        room = self.get_room(room_id)
        for k in data:
            if isinstance(data[k], datetime):
                data[k] = str(data[k])
        await room.send_personal_message(data, websocket)

    async def broadcast(self, data: dict):
        for connection in self.active_connections:
            await connection.send_json(data)

    async def broadcast_to_room(self, room_id: int, data: dict) -> None:
        room = self.get_room(room_id)

        for k in data:
            if isinstance(data[k], datetime):
                data[k] = str(data[k])
        await room.broadcast(data)


manager = ConnectionManager()
