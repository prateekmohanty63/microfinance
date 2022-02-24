from __future__ import absolute_import
import os
import django
from celery import Celery
from celery import shared_task
from django.conf import settings
from celery.schedules import crontab
from datetime import datetime, timedelta
from django.utils import timezone
from django.utils.timezone import utc
import random

# Setup django and celery to work with tasks and models
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
app = Celery('core')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
django.setup()

from home.utils import *
from home.models import *

# ------------------------------------------------------------------------------

'''
@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):

    # 15 second ping test
    sender.add_periodic_task(15.0, test_task.s(), name='Ping ping test')

@app.task
def test_task():

    # Just a test
    print('Hello from the test task!')
'''
