from fastapi import FastAPI

import sentry_sdk
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware
import auth

from base.database import engine, Base


Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth.routes)

sentry_sdk.init(dsn="https://e08875a22d804df08150988c6886b871@o504286.ingest.sentry.io/5673787") # noqa

app = SentryAsgiMiddleware(app)
