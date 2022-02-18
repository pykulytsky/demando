from fastapi import FastAPI, Depends, WebSocket, WebSocketDisconnect
from base import settings
import sentry_sdk
from starlette.requests import Request
from questions.routes import base as questions_routes

from base.database import engine, Base, get_db
from auth.routes import auth_router

from fastapi.middleware.cors import CORSMiddleware

from questions.routes.websocket import manager
from auth.backend import authenticate_via_websockets
from auth import schemas as auth_schemas
from questions.schemas import polls as polls_schemas
from questions.models import Option, Poll, Vote
from base.utils import sqlalchemy_to_pydantic


Base.metadata.create_all(bind=engine)


app = FastAPI(dependencies=[Depends(get_db)])

app.include_router(auth_router)
app.include_router(questions_routes.router)


@app.websocket('/ws/vote/{poll_id}')
async def vote_websocket(
    websocket: WebSocket,
    poll_id: str,
):
    await manager.connect_to_room(websocket, poll_id)
    db = next(get_db())
    await manager.send_personal_message_to_room(
        poll_id,
        polls_schemas.Poll.from_orm(
            Poll.manager(db).get(pk=poll_id)
        ).dict(),
        websocket
    )
    try:
        while True:
            data = await websocket.receive_json()
            user = authenticate_via_websockets(data['token'], db)
            Vote.manager(db).create(
                owner=user,
                poll=Poll.manager(db).get(pk=data['poll_id']),
                option=Option.manager(db).get(pk=data['option_id']),
            )
            await manager.broadcast_to_room(
                poll_id,
                polls_schemas.Poll.from_orm(
                    Poll.manager(db).get(pk=poll_id)
                ).dict()
            )
    except WebSocketDisconnect:
        manager.disconnect_from_room(poll_id, websocket)


origins = [
    '*'
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)


sentry_sdk.init(dsn=settings.SENTRY_DSN)


@app.middleware("http")
async def sentry_exception(request: Request, call_next):
    try:
        response = await call_next(request)
        return response
    except Exception as e:
        if request['headers'][1][1] != b'testclient':
            with sentry_sdk.push_scope() as scope:
                scope.set_context("request", request)
                scope.user = {
                    "ip_address": request.client.host,
                }
                sentry_sdk.capture_exception(e)
        raise e
