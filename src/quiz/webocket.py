from dataclasses import dataclass
from typing import List, Optional, Union

from fastapi import WebSocket
from sqlalchemy.orm import Session

from auth.backend import authenticate_via_websockets
from auth.models import User
from core.database import Base, engine
from questions.routes.websocket import ConnectionManager, Room
from quiz.models import Quiz, QuizAnonUser, Step
from quiz.schemas import steps

Base.metadata.create_all(bind=engine)


@dataclass()
class Connection:
    websocket: WebSocket
    member: Union[User, QuizAnonUser]
    host: Optional[str] = None
    is_owner: bool = False


class QuizRoom(Room):
    def __init__(self, quiz: Quiz) -> None:
        self.enter_code = quiz.enter_code
        self.quiz = quiz
        self.active_connections: List[Connection] = []
        self.current_step_iter = 0

    async def connect(
        self, webosocket: WebSocket, member: Union[User, str], is_owner: bool = False
    ):
        await webosocket.accept()
        self.active_connections.append(Connection(webosocket, member, is_owner))

    def disconnect(self, websocket: WebSocket):
        for connection in self.active_connections:
            if connection.websocket == websocket:
                self.active_connections.remove(connection)

    def get_list_of_members(self):
        members = []
        for connection in self.active_connections:
            members.append(connection.member.username)

        return members

    @property
    def owner_in_room(self) -> bool:
        for connection in self.active_connections:
            if connection.is_owner:
                return True

        return False

    def is_owner(self, user) -> bool:
        if self.quiz.owner == user:
            return True
        return False

    async def broadcast(self, data: dict, except_owner: bool = False):
        for connection in self.active_connections:
            await connection.websocket.send_json(data)

    async def send_message_to_owner(self, data: dict):
        for connection in self.active_connections:
            if connection.is_owner:
                await self.send_personal_message(connection.websocket)


class QuizConnectionManager(ConnectionManager):
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.rooms: List[QuizRoom] = []

    async def connect_to_room(
        self, websocket: WebSocket, enter_code: str, token: str, db: Session
    ):
        if "username:" in token:
            member = QuizAnonUser.manager(db).get(username=token.split(":")[1])
        else:
            member = authenticate_via_websockets(token, db)
        quiz = Quiz.manager(db).get(enter_code=enter_code)
        connected = False
        for room in self.rooms:
            if enter_code == room.enter_code:
                connected = True
                if member == quiz.owner:
                    await room.connect(websocket, member, is_owner=True)
                else:
                    await room.connect(websocket, member)

        if not connected:
            room = QuizRoom(quiz)
            self.rooms.append(room)
            if member == quiz.owner:
                await room.connect(websocket, member, is_owner=True)
            else:
                await room.connect(websocket, member)
        self.active_connections.append(websocket)

    def get_room(self, enter_code: str) -> Union[QuizRoom, None]:
        for room in self.rooms:
            if enter_code == room.enter_code:
                return room

    def disconnect_from_room(self, enter_code: str, websocket: WebSocket):
        room = self.get_room(enter_code)
        room.disconnect(websocket)

        if len(room.active_connections) == 0:
            self.rooms.remove(room)

    async def send_personal_message_to_room(
        self, enter_code: str, data: dict, websocket: WebSocket
    ):
        room = self.get_room(enter_code)
        await room.send_personal_message(data, websocket)

    async def broadcast_to_room(self, enter_code: str, data: dict) -> None:
        room = self.get_room(enter_code)
        await room.broadcast(data)

    async def broadcast_to_members(self, enter_code: str, data: dict) -> None:
        """Send data to all the members except owner."""  # TODO fix room.broadcast to remove owner from receivers list
        room = self.get_room(enter_code)
        await room.broadcast(data, except_owner=True)

    async def broadcast_list_of_members(self, enter_code: str) -> None:
        """Send to all the members list of members."""
        room = self.get_room(enter_code)
        members = room.get_list_of_members()
        await room.broadcast({"members": members})

    async def broadcast_next_step(
        self,
        enter_code: str,
        db: Session,
        step: int = 0,
    ):
        room = self.get_room(enter_code)
        current_step = room.quiz.steps[room.current_step_iter]

        step_data = steps.StepWebsocket(
            pk=current_step.pk,
            title=current_step.title,
            done=current_step.done,
            options=[option.__dict__ for option in current_step.options],
        )
        data = {"step_number": room.current_step_iter + 1, "step": step_data.dict()}

        await room.broadcast(data)

        Step.manager(db).update(pk=current_step.pk, done=True)
        room.current_step_iter += 1

    def get_quiz_results(self, enter_code: str, db: Session):
        quiz = Quiz.manager(db).get(enter_code=enter_code)
        results = {}
        for step in quiz.steps:
            for option in step.options:
                for answer in option.answers:
                    try:
                        if answer.member is not None:
                            if results.get(answer.member.username, False):
                                results.update(
                                    {
                                        answer.member.username: int(
                                            results[answer.member.username]
                                        )
                                        + int(answer.rank)
                                    }
                                )
                            else:
                                results.update({answer.member.username: answer.rank})
                        else:
                            if results.get(answer.anon_member.username, False):
                                results.update(
                                    {
                                        answer.anon_member.username: int(
                                            results[answer.anon_member.username]
                                        )
                                        + int(answer.rank)
                                    }
                                )
                            else:
                                results.update(
                                    {answer.anon_member.username: answer.rank}
                                )
                    except AttributeError:
                        continue

        return results


quiz_manager = QuizConnectionManager()
