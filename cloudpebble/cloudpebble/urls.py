from django.conf.urls import include, url
from django.conf.urls.static import static
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    # Examples:
    # url(r'^$', 'cloudpebble.views.home', name='home'),
    # url(r'^cloudpebble/', include('cloudpebble.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
     url(r'^robots\.txt', include('robots.urls')),
     url(r'^admin/', include(admin.site.urls)),
     url(r'^ide/', include('ide.urls', namespace='ide')),
     url(r'^accounts/', include('site_auth.urls')), # Namespacing this breaks things.
     url(r'^qr/', include('qr.urls', namespace='qr')),
     url(r'^', include('root.urls', namespace='root')),
     url(r'', include('social_django.urls', namespace='social')),
     url(r'^i18n/', include('django.conf.urls.i18n'))
]
