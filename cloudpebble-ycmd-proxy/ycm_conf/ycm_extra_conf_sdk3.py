from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from future import standard_library
standard_library.install_aliases()
from builtins import *
import os

if os.environ['PLATFORM'] == 'basalt':
    def FlagsForFile(filename, **kwargs):
        return {{
            'flags': [
                '-std=c11',
                '-x',
                'c',
                '-Wall',
                '-Wextra',
                '-Werror',
                '-Wno-unused-parameter',
                '-Wno-error=unused-function',
                '-Wno-error=unused-variable',
                '-I{sdk}/pebble/basalt/include',
                '-I{here}/build',
                '-I{here}',
                '-I{here}/build/src',
                '-I{here}/src',
                '-I{here}/libraries/include',
                '-isystem',
                '{stdlib}',
                '-DRELEASE',
                '-DPBL_PLATFORM_BASALT',
                '-DPBL_COLOR',
                '-DPBL_SDK_3',
                '-DPBL_RECT',
                '-DPBL_COMPASS',
                '-DPBL_HEALTH',
                '-DPBL_SMARTSTRAP',
                '-DPBL_SMARTSTRAP_POWER',
                '-DPBL_MICROPHONE',
                '-D_TIME_H_',
            ],
            'do_cache': True,
        }}
elif os.environ['PLATFORM'] == 'aplite':
    def FlagsForFile(filename, **kwargs):
        return {{
            'flags': [
                '-std=c11',
                '-x',
                'c',
                '-Wall',
                '-Wextra',
                '-Werror',
                '-Wno-unused-parameter',
                '-Wno-error=unused-function',
                '-Wno-error=unused-variable',
                '-I{sdk}/pebble/aplite/include',
                '-I{here}/build',
                '-I{here}',
                '-I{here}/build/src',
                '-I{here}/src',
                '-I{here}/libraries/include',
                '-isystem',
                '{stdlib}',
                '-DRELEASE',
                '-DPBL_PLATFORM_APLITE',
                '-DPBL_BW',
                '-DPBL_RECT',
                '-DPBL_SDK_3',
                '-DPBL_COMPASS'
            ],
            'do_cache': True,
        }}
elif os.environ['PLATFORM'] == 'chalk':
    def FlagsForFile(filename, **kwargs):
        return {{
            'flags': [
                '-std=c11',
                '-x',
                'c',
                '-Wall',
                '-Wextra',
                '-Werror',
                '-Wno-unused-parameter',
                '-Wno-error=unused-function',
                '-Wno-error=unused-variable',
                '-I{sdk}/pebble/chalk/include',
                '-I{here}/build',
                '-I{here}',
                '-I{here}/build/src',
                '-I{here}/src',
                '-I{here}/libraries/include',
                '-isystem',
                '{stdlib}',
                '-DRELEASE',
                '-DPBL_PLATFORM_CHALK',
                '-DPBL_COLOR',
                '-DPBL_SDK_3',
                '-DPBL_ROUND',
                '-DPBL_COMPASS',
                '-DPBL_HEALTH',
                '-DPBL_SMARTSTRAP',
                '-DPBL_SMARTSTRAP_POWER',
                '-DPBL_MICROPHONE',
                '-D_TIME_H_',
            ],
            'do_cache': True,
        }}
elif os.environ['PLATFORM'] == 'diorite':
    # TODO: Diorite - is this all correct?
    def FlagsForFile(filename, **kwargs):
        return {{
            'flags': [
                '-std=c11',
                '-x',
                'c',
                '-Wall',
                '-Wextra',
                '-Werror',
                '-Wno-unused-parameter',
                '-Wno-error=unused-function',
                '-Wno-error=unused-variable',
                '-I{sdk}/pebble/diorite/include',
                '-I{here}/build',
                '-I{here}',
                '-I{here}/build/src',
                '-I{here}/src',
                '-I{here}/libraries/include',
                '-isystem',
                '{stdlib}',
                '-DRELEASE',
                '-DPBL_PLATFORM_DIORITE',
                '-DPBL_BW',
                '-DPBL_SDK_3',
                '-DPBL_RECT',
                '-DPBL_HEALTH',
                '-DPBL_SMARTSTRAP',
                '-DPBL_MICROPHONE',
                '-D_TIME_H_',
            ],
            'do_cache': True,
        }}

else:
    raise Exception("Need a platform.")
