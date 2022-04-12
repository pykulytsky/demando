import sys

import sentry_sdk
from fastapi import Depends, FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from starlette.requests import Request

from auth.backend import authenticate_via_websockets
from auth.routes import auth_router
from base import settings
from base.database import Base, engine, get_db
from questions.models import Option, Poll, Vote
from questions.routes import base as questions_routes
from questions.routes.websocket import manager
from questions.schemas import polls as polls_schemas
from tests.test_database import TestSessionLocal

Base.metadata.create_all(bind=engine)


app = FastAPI(dependencies=[Depends(get_db)])

app.include_router(auth_router)
app.include_router(questions_routes.router)


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
