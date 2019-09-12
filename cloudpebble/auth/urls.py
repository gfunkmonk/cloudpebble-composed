from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from future import standard_library
standard_library.install_aliases()
from builtins import *
from django.conf.urls import patterns, url, include
from django.conf import settings

from auth import views

reg_view = views.IdeRegistrationMissingView.as_view() if settings.SOCIAL_AUTH_PEBBLE_REQUIRED else views.IdeRegistrationView.as_view()

urlpatterns = patterns(
    '',
    url(r'^register/?$', reg_view, name="registration_register"),
    url(r'^logout/?$', views.logout_view, name="logout"),
    url(r'^api/login$', views.login_action, name="login"),
    url(r'', include('registration.backends.simple.urls'))
)
