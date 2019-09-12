from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from future import standard_library
standard_library.install_aliases()
from builtins import *
import json

from waflib.Configure import conf


@conf
def configure_appinfo(ctx, transforms):
    with open('appinfo.json', 'r') as appinfo_file:
        appinfo_json = json.load(appinfo_file)

    for transform in transforms:
        transform(appinfo_json)

    with open('appinfo.json', 'w') as appinfo_file:
        json.dump(appinfo_json, appinfo_file, indent=2, sort_keys=True, separators=(',', ': '))
