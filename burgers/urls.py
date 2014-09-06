# -*- coding: utf-8 -*-
#Copyright © Marina Gerace. All rights reserved
from django.conf.urls import *
from views import BurgerCreate

urlpatterns = patterns('burgers.views',
    #homepage
	url(r'^$', BurgerCreate.as_view(), name = 'create_burger'),
	(r'^burger/', 'show_ingredients', {}, 'show_ingredients'),
	)
