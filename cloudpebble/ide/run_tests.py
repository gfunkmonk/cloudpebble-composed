#!/ usr/bin/env python
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from future import standard_library
standard_library.install_aliases()
from builtins import *
import os
import sys

if __name__ == "__main__":
    sys.path.append("../")
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cloudpebble.settings")

    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv.append("test"))
