import sys

import shlex
import subprocess
from django.core.management.base import BaseCommand
from django.utils import autoreload


class Command(BaseCommand):
    def handle(self, *args, **options):
        autoreload.main(self._restart_celery)

    @classmethod
    def _restart_celery(cls):
        if sys.platform == "win32":
            cls.run('taskkill /f /t /im celery.exe')
            cls.run('celery -A phoenix worker --loglevel=info --pool=solo')
        else:  # probably ok for linux2, cygwin and darwin. Not sure about os2, os2emx, riscos and atheos
            cls.run('pkill celery')
            cls.run('celery worker -l info -A foo')

    @staticmethod
    def run(cmd):
        subprocess.call(shlex.split(cmd))
