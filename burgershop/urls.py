# -*- coding: utf-8 -*-
#Copyright © Marina Gerace. All rights reserved
from django.conf.urls import patterns, include, url
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', include('burgers.urls')),
    url(r'^ingredients/', include('burgers.urls')),
    url(r'^checkout/', include('checkout.urls')),
    url(r'^accounts/', include('accounts.urls')),
)

if settings.DEBUG:
    urlpatterns = patterns('',
               url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
                   {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
               url(r'', include('django.contrib.staticfiles.urls')),
               ) + urlpatterns
