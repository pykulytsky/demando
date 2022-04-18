from celery import Celery
from celery.utils.log import get_task_logger

app = Celery("tasks", broker="redis://localhost:6379")
app.config_from_object("tasks.celeryconfig")
app.autodiscover_tasks()
celery_log = get_task_logger(__name__)
