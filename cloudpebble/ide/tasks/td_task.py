from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from future import standard_library
standard_library.install_aliases()
from builtins import *
from celery import task
from django.conf import settings

import requests

__author__ = 'katharine'


@task(ignore_result=True)
def td_add_events(event):
    result = requests.post(settings.TD_URL, data=event)
    result.raise_for_status()
