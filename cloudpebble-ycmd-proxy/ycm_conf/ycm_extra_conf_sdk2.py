from __future__ import absolute_import
import os

def FlagsForFile(filename, **kwargs):
    return {{
        'flags': [
            '-std=c11',
            '-x',
            'c',
            '-m32',
            '-Wall',
            '-Wextra',
            '-Werror',
            '-Wno-unused-parameter',
            '-Wno-error=unused-function',
            '-Wno-error=unused-variable',
            '-I{sdk}/pebble/include',
            '-I{here}/build',
            '-I{here}',
            '-I{here}/build/src',
            '-I{here}/src',
            '-isystem',
            '{stdlib}',
            '-DRELEASE',
        ],
        'do_cache': True,
    }}
