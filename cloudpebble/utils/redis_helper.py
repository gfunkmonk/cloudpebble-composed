from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from future import standard_library
standard_library.install_aliases()
from builtins import *
__author__ = 'katharine'

import redis
from django.conf import settings

redis_client = redis.from_url(settings.REDIS_URL)
