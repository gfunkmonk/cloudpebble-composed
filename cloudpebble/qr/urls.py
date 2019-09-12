from __future__ import absolute_import
from django.conf.urls import patterns, url

from qr import views

urlpatterns = patterns(
    '',
    url('$^', views.render, name='render')
)
