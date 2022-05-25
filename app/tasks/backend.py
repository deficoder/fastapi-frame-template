from syslog import LOG_LOCAL0
from loguru import logger
from config.settings import LOGGING_LEVEL, SETTINGS

from celery import Celery

from kombu import Exchange, Queue

# Celery 
app = Celery('tasks', broker=SETTINGS.CELERY_BROKER, backend=SETTINGS.CELERY_BACKEND)
app.conf.update(result_expires=60, task_serializer='json', accept_content=['json'], result_serializer='json', timezone='Asia/Shanghai', enable_utc=False)

app.conf.task_queues = (
    Queue('default', Exchange('default', type='direct'), routing_key='default'),
)
app.conf.task_default_queue = 'default'
app.conf.task_default_exchange_type = 'direct'
app.conf.task_default_routing_key = 'default'

app.autodiscover_tasks()

@app.on_after_configure.connect
def add_periodic(**kargs):
    app.add_periodic_task(SETTINGS.CELERY_INTERVAL, periodic_task.s(), name='exec periodic task every {}'.format(SETTINGS.CELERY_INTERVAL))

@app.task(name='periodic_task')
def periodic_task():
    logger.log(LOGGING_LEVEL, 'Hello periodic_task')

@app.task(name='remote_task')
def remote_task():
    logger.log(LOG_LOCAL0, 'remote task')