# encoding: utf-8
# Django settings for cloudpebble project.

import sys
import os
import socket
import dj_database_url

_environ = os.environ

DEBUG = _environ.get('DEBUG', '') != ''
VERBOSE = DEBUG or (_environ.get('VERBOSE', '') != '')
TESTING = 'test' in sys.argv
TRAVIS = 'TRAVIS' in _environ and os.environ["TRAVIS"] == "true"
TEMPLATE_DEBUG = DEBUG

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
ADMINS = (
    ('admin', 'admin@cloudpebble.tk'),
)
MANAGERS = ADMINS

DEFAULT_FROM_EMAIL = _environ.get('FROM_EMAIL', 'CloudPebble <admin@cloudpebble.tk>')

ON_CLOUDFLARE = _environ.get('CLOUDFLARE') != ''
if ON_CLOUDFLARE:
    SECURE_PROXY_SSL_HEADER = ('HTTP_CF_VISITOR', '{"scheme":"https"}')
else:
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

MANAGERS = ADMINS

if TRAVIS:
    DATABASES = {
        'default': {
            'ENGINE':   'django.db.backends.postgresql_psycopg2',
            'NAME':     'travisci',
            'USER':     'postgres',
            'PASSWORD': '',
            'HOST':     'localhost',
            'PORT':     '',
        }
    }
elif 'DATABASE_URL' not in _environ:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'postgres',
            'USER': 'postgres',
            'HOST': 'postgres',
            'PORT': 5432,
        }
    }
else:
    DATABASES = {
        'default': dj_database_url.config()
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

PROJECT_PATH = os.path.dirname(os.path.abspath(__file__)) + '/../'

LANGUAGE_COOKIE_NAME = 'cloudpebble_language'

#TEMPLATE_CONTEXT_PROCESSORS = (
#    "django.contrib.auth.context_processors.auth",
#    "django.core.context_processors.debug",
#    "django.core.context_processors.i18n",
#    "django.core.context_processors.media",
#    "django.core.context_processors.static",
#    "django.core.context_processors.tz",
#    "django.contrib.messages.context_processors.messages",
#    "social.apps.django_app.context_processors.backends",
#    "social.apps.django_app.context_processors.login_redirect",
#)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
           os.path.join(BASE_DIR, "ide/templates"),
           os.path.join(BASE_DIR, "root/templates"),
         ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                #'social.apps.django_app.context_processors.backends',
                #'social.apps.django_app.context_processors.login_redirect',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
             ],
        },
    },
]
# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ['*']

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/New_York'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

LANGUAGES = (
    ('en', 'English'),
    ('es', 'Spanish'),
    ('fr', 'French'),
    ('de', 'German'),
    ('zh-cn', 'Chinese (simplified'),
    ('zh-tw', 'Chinese (traditional)'),

)

LOCALE_PATHS = (os.getcwd() + "/locale",)

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = os.getcwd() + '/user_data/build_results/'

SIMPLYJS_ROOT = os.getcwd() + '/ext/simplyjs/'
PEBBLEJS_ROOT = os.getcwd() + '/ext/pebblejs/'
C_PRELOAD_ROOT = os.getcwd() + '/c-preload/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = _environ.get('MEDIA_URL', 'http://localhost:8001/builds/')

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

PUBLIC_URL = _environ.get('PUBLIC_URL', 'http://localhost:8000/') # This default is completely useless.

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
     os.path.join(os.path.dirname(__file__), '..', 'bower_components'),
)

# List of finder classes that know how to find static files in
# various locations.

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'djangobower.finders.BowerFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

BOWER_INSTALLED_APPS = (
    'https://github.com/krisk/Fuse.git#a546cb3aa2a845e4f4cb2460ad94e0b92ccbe407',
    'jquery#~2.1.3',
    'underscore',
    'backbone',
    'text-encoding',
    'jshint/jshint',
    'html.sortable#~0.3.1',
    'gfunkmonk/jquery-textext',
    'CodeMirror#5.15.2',
    'bluebird#~3.3.5',
    'kanaka/noVNC#0.5.1',
    'https://code.jquery.com/jquery-migrate-1.4.1.js',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = _environ.get('SECRET_KEY', None)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

if not DEBUG:
    STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.CachedStaticFilesStorage'

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

AUTHENTICATION_BACKENDS = (
    'site_auth.pebble.PebbleOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)

SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.auth_allowed',
    'site_auth.pebble.merge_user', # formerly social.pipeline.social_auth.social_user
    'social_core.pipeline.user.get_username',
    'social_core.pipeline.user.create_user',
    'social_core.pipeline.social_auth.associate_user',
    'site_auth.pebble.clear_old_login',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details'
)

SOCIAL_AUTH_PEBBLE_KEY = _environ.get('PEBBLE_AUTH_KEY', None)
SOCIAL_AUTH_PEBBLE_SECRET = _environ.get('PEBBLE_AUTH_SECRET', None)

SOCIAL_AUTH_PEBBLE_ROOT_URL = _environ.get('PEBBLE_AUTH_URL', None)
PEBBLE_AUTH_ADMIN_TOKEN = _environ.get('PEBBLE_AUTH_ADMIN_TOKEN', None)

SHOULD_BE_SECURE = _environ.get('EXPECT_SSL', '') != ''

SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = SHOULD_BE_SECURE
CSRF_COOKIE_SECURE = SHOULD_BE_SECURE

SOCIAL_AUTH_PEBBLE_REQUIRED = 'PEBBLE_AUTH_REQUIRED' in _environ

SOCIAL_AUTH_ADMIN_USER_SEARCH_FIELDS = ['username', 'first_name', 'email']

SOCIAL_AUTH_STRATEGY = 'social_django.strategy.DjangoStrategy'
SOCIAL_AUTH_STORAGE = 'social_django.models.DjangoStorage'

SOCIAL_AUTH_POSTGRES_JSONFIELD = True

ROOT_URLCONF = 'cloudpebble.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'cloudpebble.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
     os.path.join(os.path.dirname(__file__), '..', 'ide/templates'),
     os.path.join(os.path.dirname(__file__), '..', 'root/templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'admin_interface',
    #'flat',
    'flat_responsive',
    'colorfield',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    #'social.apps.django_app.default',
    'social_django',
    'ide',
    'site_auth',
    'root',
    'qr',
    #'south',
    #'djcelery',
    'registration',
    'djangobower',
    'robots',
    'django_celery_beat',
    'redisboard',
    'django_extensions',
)
# This logging config prints:
# INFO logs from django
# INFO or DEBUG logs from 'ide', depending on whether DEBUG=True
# all WARNING logs from any sources
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt': "%d/%b/%Y %H:%M:%S"
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True
        },
        'ide': {
            'handlers': ['console'],
            'level': 'DEBUG' if VERBOSE else 'INFO',
            'propagate': True
        },
        'root': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True
        },
        '': {
            'handlers': ['console'],
            'level': 'WARNING',
            'propagate': False
        }
    }
}

if TESTING:
    # Many tests make deliberately broken requests. If this line is not present,
    # the log output during tests gets flooded with 'expected' exceptions.
    LOGGING['loggers']['django.request'] = {'level': 'CRITICAL'}

REDIS_URL = _environ.get('REDIS_URL', None) or _environ.get('REDISCLOUD_URL', 'redis://redis:6379')

BROKER_URL = REDIS_URL + '/1'
CELERY_RESULT_BACKEND = BROKER_URL
CELERY_ACCEPT_CONTENT = ['json', 'pickle']
CELERY_TASK_SERIALIZER = 'pickle'
CELERY_RESULT_SERIALIZER = 'pickle'
##CELERY_ACCEPT_CONTENT = ['application/json']
##CELERY_TASK_SERIALIZER = 'json'
##CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'America/New_York'
CELERY_ENABLE_UTC = False
CELERYBEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'

CELERYD_HIJACK_ROOT_LOGGER = False

CELERYD_TASK_TIME_LIMIT = int(_environ.get('CELERYD_TASK_TIME_LIMIT', 620))
CELERYD_TASK_SOFT_TIME_LIMIT = int(_environ.get('CELERYD_TASK_SOFT_TIME_LIMIT', 600))

BROKER_POOL_LIMIT = int(_environ.get('BROKER_POOL_LIMIT', 10))

LOGIN_REDIRECT_URL = '/ide/'

LOGIN_URL = '/#login'


FILE_STORAGE = os.getcwd() + '/user_data/'

CHROOT_ROOT = None

DEFAULT_TEMPLATE = None

EXPORT_DIRECTORY = os.getcwd() + '/user_data/export/'

EXPORT_ROOT = _environ.get('EXPORT_ROOT', 'http://localhost:8001/export/')

GITHUB_CLIENT_ID = _environ.get('GITHUB_ID', None)
GITHUB_CLIENT_SECRET = _environ.get('GITHUB_SECRET', None)

GITHUB_HOOK_TEMPLATE = _environ.get('GITHUB_HOOK', 'http://cloudpebble.tk/ide/project/%(project)d/github/push_hook?key=%(key)s')

SDK2_PEBBLE_WAF = _environ.get('SDK2_PEBBLE_WAF', '/sdk2/pebble/waf')
SDK3_PEBBLE_WAF = _environ.get('SDK3_PEBBLE_WAF', '/sdk3/pebble/waf')

NPM_BINARY = _environ.get('NPM_BINARY', 'npm')

ARM_CS_TOOLS = _environ.get('ARM_CS_TOOLS', '/arm-cs-tools/bin/')

TD_URL = _environ.get('TD_URL', None)
TD_ENABLED = _environ.get('TD_ENABLED', False)

MAILCHIMP_API_KEY = _environ.get('MAILCHIMP_API_KEY', None)
MAILCHIMP_LIST_ID = _environ.get('MAILCHIMP_LIST_ID', None)

AWS_ENABLED = 'AWS_ENABLED' in _environ
AWS_ACCESS_KEY_ID = _environ.get('AWS_ACCESS_KEY_ID', None)
AWS_SECRET_ACCESS_KEY = _environ.get('AWS_SECRET_ACCESS_KEY', None)

AWS_S3_SOURCE_BUCKET = _environ.get('AWS_S3_SOURCE_BUCKET', 'source.cloudpebble.net')
AWS_S3_BUILDS_BUCKET = _environ.get('AWS_S3_BUILDS_BUCKET', 'builds.cloudpebble.net')
AWS_S3_EXPORT_BUCKET = _environ.get('AWS_S3_EXPORT_BUCKET', 'export.cloudpebble.net')
AWS_S3_HOST = _environ.get('AWS_S3_HOST', None)
AWS_S3_FAKE_S3 = _environ.get('AWS_S3_FAKE_S3', None)

TYPOGRAPHY_CSS = _environ.get('TYPOGRAPHY_CSS', None)

LIBPEBBLE_PROXY = _environ.get('LIBPEBBLE_PROXY', None)

YCM_URLS = _environ.get('YCM_URLS', 'http://localhost:8002/').split(',')
COMPLETION_CERTS = _environ.get('COMPLETION_CERTS', os.getcwd() + '/completion-certs.crt')

QEMU_URLS = _environ.get('QEMU_URLS', 'http://qemu/').split(',')
QEMU_LAUNCH_AUTH_HEADER = _environ.get('QEMU_LAUNCH_AUTH_HEADER', 'secret')
QEMU_LAUNCH_TIMEOUT = int(_environ.get('QEMU_LAUNCH_TIMEOUT', 25))

PHONE_SHORTURL = _environ.get('PHONE_SHORTURL', 'cpbl.io')

WAF_NODE_PATH = _environ.get('WAF_NODE_PATH', None)

ROBOTS_USE_SITEMAP = False
ROBOTS_USE_SCHEME_IN_HOST = True
ROBOTS_CACHE_TIMEOUT = 60*60*24

USE_THOUSAND_SEPARATOR = True

#import djcelery
#djcelery.setup_loader()

# import local settings
try:
    from settings_local import *
except ImportError:
    print "No local settings overrides."
    pass

socket.setdefaulttimeout(int(_environ.get("DEFAULT_SOCKET_TIMEOUT", 10)))

# Don't keep these hanging around in the environment.
if not DEBUG:
    for key in _environ.keys():
        # We need these ones to run.
        if key in {'PATH', 'TZ', 'RUN_MAIN', 'CELERY_LOADER', 'DJANGO_SETTINGS_MODULE', 'DEBUG', 'C_FORCE_ROOT'}:
            continue
        del _environ[key]
