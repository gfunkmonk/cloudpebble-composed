from __future__ import absolute_import
import os
from celery import Celery
from celery.signals import setup_logging

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cloudpebble.settings')

from django.conf import settings  # noqa

app = Celery('cloudpebble')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
##app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
##app.autodiscover_tasks()

@setup_logging.connect
def config_loggers(*args, **kwags):
    from logging.config import dictConfig
    from django.conf import settings
    dictConfig(settings.LOGGING)

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
