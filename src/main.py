import logging
import sys

import aiofiles
import sentry_sdk
from fastapi import (Depends, FastAPI, File, UploadFile, WebSocket,
                     WebSocketDisconnect)
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from logtail import LogtailHandler
from sqlalchemy.orm import Session
from starlette.requests import Request

from auth.backend import authenticate, authenticate_via_websockets
from auth.models import User
from auth.routes import auth_router
from core import settings
from core.database import Base, engine, get_db
from logger import http_logger
from questions.models import Option, Poll, Vote
from questions.routes import base as questions_routes
from questions.routes.websocket import manager
from questions.schemas import polls as polls_schemas
from quiz.models import Answer, QuizAnonUser, StepOption
from quiz.routes import base as quizzes_router
from quiz.webocket import quiz_manager
from tests.test_database import TestSessionLocal

Base.metadata.create_all(bind=engine)

app = FastAPI(dependencies=[Depends(get_db)])

app.mount("/static", StaticFiles(directory="src/static"), name="static")


def logtail_ready():
    handler = LogtailHandler(source_token=settings.LOGTAIL_TOKEN)

    app.logger = logging.getLogger(__name__)
    app.logger.handlers = [handler]
    app.logger.setLevel(logging.INFO)

    app.logger.info("logtail is ready")
    app.logger.critical("test")


app.include_router(auth_router)
app.include_router(questions_routes.router)
app.include_router(quizzes_router.router)

app.add_event_handler("startup", logtail_ready)


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
                try:
                    user = authenticate_via_websockets(data["token"], db)
                except KeyError:
                    user = False
                if user:
                    if data.get("multiply", False):
                        for option in data["options"]:
                            Vote.manager(db).create(
                                owner=user,
                                poll=Poll.manager(db).get(pk=data["poll_id"]),
                                option=Option.manager(db).get(pk=option),
                            )
                    else:
                        Vote.manager(db).create(
                            owner=user,
                            poll=Poll.manager(db).get(pk=data["poll_id"]),
                            option=Option.manager(db).get(pk=data["option_id"]),
                        )
                elif data.get("ip_address", False):
                    if data.get("multiply", False):
                        for option in data["options"]:
                            Vote.manager(db).create(
                                owner_host=data["ip_address"],
                                poll=Poll.manager(db).get(pk=data["poll_id"]),
                                option=Option.manager(db).get(pk=option),
                            )
                    else:
                        Vote.manager(db).create(
                            owner_host=data["ip_address"],
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
                await manager.disconnect_from_room(poll_id, websocket)
                db.close()
    except WebSocketDisconnect:
        await manager.disconnect_from_room(poll_id, websocket)
        db.close()


@app.websocket("/ws/quiz/{enter_code}/{token}")
async def quiz(websocket: WebSocket, enter_code: str, token: str):

    db = next(get_db())
    if "pytest" in sys.argv[0]:
        db = TestSessionLocal()

    if "username:" in token:
        user = QuizAnonUser.manager(db).create(username=token.split(":")[1])
    else:
        user = authenticate_via_websockets(token, db)
    room = quiz_manager.get_room(enter_code)
    if room:
        # if not room.is_owner(user):
        #     if not room.owner_in_room:
        #         await websocket.close(code=1007)
        #         raise WebSocketDisconnect()
        for connection in room.active_connections:
            if connection.member == user:
                await websocket.close()
                raise WebSocketDisconnect()
            if connection.member.username == user.username:
                await websocket.send_json({"type": "username"})
                await websocket.close(code=1007)
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
                            enter_code, db, int(data["step"])
                        )
                    except IndexError:
                        await quiz_manager.broadcast_to_room(
                            enter_code,
                            data={
                                "action": "finish",
                                "final_results": quiz_manager.get_quiz_results(
                                    enter_code, db
                                ),
                            },
                        )

            if data.get("answer", False):
                step_option = StepOption.manager(db).get(
                    pk=data["answer"]["option"]["pk"]
                )
                rank = 0
                if step_option.is_right:
                    rank = round(
                        int(data["answer"]["time"])
                        * 1000
                        / step_option.step.quiz.seconds_per_answer
                    )
                if isinstance(user, User):
                    Answer.manager(db).create(
                        member=user,
                        step_option=step_option,
                        time_to_estimate=data["answer"]["time"],
                        rank=rank,
                    )
                else:
                    Answer.manager(db).create(
                        anon_member=user,
                        step_option=step_option,
                        time_to_estimate=data["answer"]["time"],
                        rank=rank,
                    )
                print(f"{websocket=}, {rank=}")
                await quiz_manager.send_personal_message(
                    data={"results": rank}, websocket=websocket
                )

    except WebSocketDisconnect:
        if isinstance(user, User):
            if user.email == "temp.email.quiz@temp.quiz":
                User.manager(db).delete(user)
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


@app.middleware("http")
async def logtail(request: Request, call_next):
    try:
        response = await call_next(request)
        http_logger.info(request, response)
        return response
    except Exception as e:
        if request["headers"][1][1] != b"testclient":
            http_logger.error(request, e)
        raise e


@app.post("/uploadfile/")
async def create_upload_file(
    request: Request,
    user: auth_router.get_schema = Depends(authenticate),
    db: Session = Depends(get_db),
    file: UploadFile = File(...)
):
    print(request.url._url[0:-11])
    async with aiofiles.open(f"src/static/{file.filename}", "wb") as out_file:
        content = await file.read()  # async read
        await out_file.write(content)  # async write

    user = User.manager(db).update(
        pk=user.pk,
        avatar=request.url._url[0:-11] + "static/" + file.filename
    )
    return {"filename": user.avatar}
