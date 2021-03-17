from fastapi import FastAPI
from fastapi.param_functions import Depends

import sentry_sdk
from starlette.requests import Request
from auth import routes as auth_routes
from questions.routes import base as questions_routes

from base.database import engine, Base, get_db


Base.metadata.create_all(bind=engine)


app = FastAPI(dependencies=[Depends(get_db)])

app.include_router(auth_routes.router)
app.include_router(questions_routes.router)

sentry_sdk.init(dsn="https://e08875a22d804df08150988c6886b871@o504286.ingest.sentry.io/5673787") # noqa


@app.middleware("http")
async def sentry_exception(request: Request, call_next):
    try:
        response = await call_next(request)
        return response
    except Exception as e:
        if request['headers'][1][1] == b'testclient':
            with sentry_sdk.push_scope() as scope:
                scope.set_context("request", request)
                user_id = "database_user_id"  # when available
                scope.user = {
                    "ip_address": request.client.host,
                    "pk": user_id
                }
                sentry_sdk.capture_exception(e)
        raise e
