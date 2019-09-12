from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from future import standard_library
standard_library.install_aliases()
from builtins import *
worker_class = 'gevent'
workers = 3


def post_fork(server, worker):
    from psycogreen.gevent import patch_psycopg
    patch_psycopg()
