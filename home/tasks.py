from celery import shared_task

from home.utils import *
from home.models import *
from accounts.models import *


@shared_task(name="Create a log")
def add_log(log_message):
    print(log_message)
    return True


