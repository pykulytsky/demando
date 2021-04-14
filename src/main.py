from fastapi import FastAPI, Depends
from base import settings
import sentry_sdk
from starlette.requests import Request

from base.database import engine, Base, get_db

from auth.routes import auth_router
from questions.routes.base import router as questions_router

from tortoise.contrib.fastapi import HTTPNotFoundError, register_tortoise


Base.metadata.create_all(bind=engine)


app = FastAPI(dependencies=[Depends(get_db)])

app.include_router(auth_router)
app.include_router(questions_router)


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

register_tortoise(
    app=app,
    config={
        'connections': {
            'default': {
                'engine': 'tortoise.backends.asyncpg',
                'credentials': {
                    'host': 'localhost',
                    'port': '5432',
                    'user': 'o_p',
                    'password': '#pragma_once',
                    'database': 'demando',
                },
                'maxsize': 100
            }
        },
        'apps': {
            'auth': {
                'models': ["auth.models"],
                'default_connection': 'default',
            },
            'questions': {
                'models': ["questions.models"],
                'default_connection': 'default',
            }
        }
    },
    generate_schemas=True,
    add_exception_handlers=True,
)
