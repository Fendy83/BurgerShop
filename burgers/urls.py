# -*- coding: utf-8 -*-
#Copyright © Marina Gerace. All rights reserved
from django.conf.urls import *

urlpatterns = patterns('burgers.views',
    #homepage
	(r'^$', 'show_ingredients', {}, 'show_ingredients'),
	)
