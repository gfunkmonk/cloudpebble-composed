__author__ = 'katharine'

from os import environ as env

YCMD_BINARY = env.get('YCMD_BINARY', "/Users/katharine/projects/ycmd/ycmd/__main__.py")
YCMD_SETTINGS = env.get('YCMD_DEFAULT_SETTINGS', "/Users/katharine/projects/ycmd/ycmd/default_settings.json")
PEBBLE_SDK2 = env.get('YCMD_PEBBLE_SDK2', "/usr/local/Cellar/pebble-sdk/2.5/")
PEBBLE_SDK3 = env.get('YCMD_PEBBLE_SDK3', "/usr/local/Cellar/pebble-sdk/2.5/")
NPM_BINARY = env.get('NPM_BINARY', 'npm')
STDLIB_INCLUDE_PATH = env.get('YCMD_STDLIB', "/usr/local/Cellar/pebble-sdk/2.5/arm-cs-tools/arm-none-eabi/include/")
DEBUG = 'DEBUG' in env
PORT = int(env.get('YCMD_PORT', 5000))
HOST = env.get('YCMD_HOST', '0.0.0.0')
SSL_ROOT = env.get('SSL_ROOT', None)
RUN_AS_USER = env.get('RUN_AS_USER', None)
