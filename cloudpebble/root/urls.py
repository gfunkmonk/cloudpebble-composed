from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from future import standard_library
standard_library.install_aliases()
from builtins import *
from django.conf.urls import patterns, url, include

from root import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^i18n/', include('django.conf.urls.i18n'))
)
