# -*- coding: utf-8 -*-
#Copyright © Marina Gerace. All rights reserved
from django.conf.urls import *

urlpatterns = patterns('django.contrib.auth.views',
                        (r'^login/$', 'login', {'template_name': 'accounts/login.html' },'login'),
                        (r'^logout/$', 'logout', {'template_name': 'accounts/loggedout.html' },'logout'),
                        )