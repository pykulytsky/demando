import sys

from core.database import get_db
from core.integrations.mailjet import MailService
from questions.models import Event
from tasks import app, celery_log
from tests.test_database import TestSessionLocal

service = MailService()


@app.task
def send_verification_mail():
    print("Hello world")


@app.task
def notify_event_statistic(event_id: int):
    db = next(get_db())
    if "pytest" in sys.argv[0]:
        db = TestSessionLocal()

    event = Event.manager(db).get(pk=event_id)
    response = service.nofity_event_owner(event)
    celery_log.info(response.json())

    return response
