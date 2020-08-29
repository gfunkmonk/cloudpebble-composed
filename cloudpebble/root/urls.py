from django.conf.urls import url, include

from root import views

from django.http import HttpResponse

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^robots\.txt', include('robots.urls')),
    url(r'^robots.txt$', lambda r: HttpResponse("User-agent: *\nDisallow: /", mimetype="text/plain")),
]
