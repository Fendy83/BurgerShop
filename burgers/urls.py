# -*- coding: utf-8 -*-
#Copyright © Marina Gerace. All rights reserved
from django.conf.urls import *
from views import BurgerCreate, ShowIngredients

urlpatterns = patterns('burgers.views',
    #homepage
	url(r'^$', BurgerCreate.as_view(), name = 'create_burger'),
	url(r'^burger/', ShowIngredients.as_view(), name = 'show_ingredients'),
	)
