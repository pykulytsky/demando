from celery import Celery


app = Celery("tasks", broker="redis://localhost:6379")
app.config_from_object('tasks.celeryconfig')
app.autodiscover_tasks()
