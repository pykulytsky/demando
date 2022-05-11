import sys

import sentry_sdk
from fastapi import Depends, FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from starlette.requests import Request

from auth.backend import authenticate_via_websockets
from auth.routes import auth_router
from core import settings
from core.database import Base, engine, get_db
from questions.models import Option, Poll, Vote
from questions.routes import base as questions_routes
from questions.routes.websocket import manager
from questions.schemas import polls as polls_schemas
from quiz.models import Answer, Step, StepOption
from quiz.routes import base as quizzes_router
from quiz.webocket import quiz_manager
from tests.test_database import TestSessionLocal

Base.metadata.create_all(bind=engine)


app = FastAPI(dependencies=[Depends(get_db)])

app.include_router(auth_router)
app.include_router(questions_routes.router)
app.include_router(quizzes_router.router)


@app.websocket("/ws/vote/{poll_id}")
async def vote_websocket(
    websocket: WebSocket,
    poll_id: str,
):
    await manager.connect_to_room(websocket, poll_id)

    db = next(get_db())
    if "pytest" in sys.argv[0]:
        db = TestSessionLocal()

    await manager.send_personal_message_to_room(
        poll_id,
        polls_schemas.Poll.from_orm(Poll.manager(db).get(pk=poll_id)).dict(),
        websocket,
    )
    try:
        while True:
            data = await websocket.receive_json()
            try:
                user = authenticate_via_websockets(data["token"], db)

                Vote.manager(db).create(
                    owner=user,
                    poll=Poll.manager(db).get(pk=data["poll_id"]),
                    option=Option.manager(db).get(pk=data["option_id"]),
                )
                await manager.broadcast_to_room(
                    poll_id,
                    polls_schemas.Poll.from_orm(
                        Poll.manager(db).get(pk=poll_id)
                    ).dict(),
                )
            except TypeError:
                manager.disconnect_from_room(poll_id, websocket)
                db.close()
    except WebSocketDisconnect:
        manager.disconnect_from_room(poll_id, websocket)
        db.close()


@app.websocket("/ws/quiz/{enter_code}/{token}")
async def quiz(websocket: WebSocket, enter_code: str, token: str):

    db = next(get_db())
    if "pytest" in sys.argv[0]:
        db = TestSessionLocal()

    user = authenticate_via_websockets(token, db)
    room = quiz_manager.get_room(enter_code)
    if room:
        for connection in room.active_connections:
            if connection.member == user:
                raise WebSocketDisconnect()

    await quiz_manager.connect_to_room(websocket, enter_code, token, db)
    await quiz_manager.broadcast_list_of_members(enter_code)
    try:
        while True:
            data = await websocket.receive_json()
            if data.get("action", False):
                if data["action"] == "start":  # start quiz
                    await quiz_manager.broadcast_next_step(enter_code, db, 0)
                if data["action"] == "next":  # next step
                    try:
                        await quiz_manager.broadcast_next_step(
                            enter_code, db, data["step"]
                        )
                    except IndexError:
                        pass  # finish
            if data.get("answer", False):
                step_option = StepOption.manager(db).get(pk=data['answer']['option']['pk'])
                rank = 0
                if step_option.is_right:
                    rank = round(int(data['answer']['time']) * 1000 / 30)
                answer = Answer.manager(db).create(
                    member=user,
                    step_option=step_option,
                    time_to_estimate=data['answer']['time'],
                    rank=rank
                )
                await quiz_manager.send_personal_message(
                    data={
                        "results": rank
                    },
                    websocket=websocket
                )

    except WebSocketDisconnect:
        quiz_manager.disconnect_from_room(enter_code, websocket)


origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


sentry_sdk.init(dsn=settings.SENTRY_DSN)


@app.middleware("http")
async def sentry_exception(request: Request, call_next):
    try:
        response = await call_next(request)
        return response
    except Exception as e:
        if request["headers"][1][1] != b"testclient":
            with sentry_sdk.push_scope() as scope:
                scope.set_context("request", request)
                scope.user = {
                    "ip_address": request.client.host,
                }
                sentry_sdk.capture_exception(e)
        raise e
