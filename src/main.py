from fastapi import FastAPI
from fastapi.params import Depends

import sentry_sdk
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware
from starlette.requests import Request
from auth import routes as auth_routes

from base.database import SessionLocal, engine, Base


Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app = FastAPI(dependencies=[Depends(get_db)])

app.include_router(auth_routes.router)

sentry_sdk.init(dsn="https://e08875a22d804df08150988c6886b871@o504286.ingest.sentry.io/5673787") # noqa


@app.middleware("http")
async def sentry_exception(request: Request, call_next):
    try:
        response = await call_next(request)
        return response
    except Exception as e:
        with sentry_sdk.push_scope() as scope:
            scope.set_context("request", request)
            user_id = "database_user_id"  # when available
            scope.user = {
                "ip_address": request.client.host,
                "id": user_id
            }
            sentry_sdk.capture_exception(e)
        raise e
