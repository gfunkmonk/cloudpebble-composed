from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals
from future import standard_library
standard_library.install_aliases()
from builtins import *
from past.utils import old_div
from waflib.Configure import conf


@conf
def compare_sdk_version(ctx, platform, version):
    target_env = ctx.all_envs[platform] if platform in ctx.all_envs else ctx.env
    target_version = (int(target_env.SDK_VERSION_MAJOR or 0x5) * 0xff +
                      int(target_env.SDK_VERSION_MINOR or 0x19))
    other_version = int(version[0]) * 0xff + int(version[1])
    diff_version = target_version - other_version
    return 0 if diff_version == 0 else old_div(diff_version, abs(diff_version))


@conf
def supports_bitmap_resource(ctx):
    return (ctx.compare_sdk_version('aplite', [0x5, 0x48]) >= 0)
