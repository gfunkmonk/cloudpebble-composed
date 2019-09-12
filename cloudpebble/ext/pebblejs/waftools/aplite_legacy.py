from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from future import standard_library
standard_library.install_aliases()
from builtins import *
from waflib.Configure import conf


@conf
def appinfo_bitmap_to_png(ctx, appinfo_json):
    if not ctx.supports_bitmap_resource():
        for res in appinfo_json['resources']['media']:
            if res['type'] == 'bitmap':
                res['type'] = 'png'
