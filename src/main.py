from fastapi import FastAPI, Depends
from base import settings
import sentry_sdk
from starlette.requests import Request
from questions.routes import base as questions_routes

from base.database import engine, Base, get_db
from auth.routes import auth_router


Base.metadata.create_all(bind=engine)


app = FastAPI(dependencies=[Depends(get_db)])

app.include_router(auth_router)
app.include_router(questions_routes.router)


sentry_sdk.init(dsn=settings.SENTRY_DSN)


@app.middleware("http")
async def sentry_exception(request: Request, call_next):
    try:
        response = await call_next(request)
        return response
    except Exception as e:
        if request['headers'][1][1] != b'testclient':
            print('captured')
            with sentry_sdk.push_scope() as scope:
                scope.set_context("request", request)
                scope.user = {
                    "ip_address": request.client.host,
                }
                sentry_sdk.capture_exception(e)
        raise e
