# -*- coding: utf-8 -*-
#Copyright © Marina Gerace. All rights reserved
from django.conf.urls import *
from views import OrderUpdate
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView


urlpatterns = patterns('checkout.views',
	(r'^checkout/$', 'order', {}, 'order'),
	(r'^order_done/$', 'order_done', {}, 'order_done'),
	(r'^orders/$', 'show_orders', {}, 'show_orders'),
    (r'^orders/(?P<status>[-\w]+)/$', 'show_orders',	{},'show_orders'),
    (r'^success/', TemplateView.as_view(template_name="checkout/success.html")),
    (r'^error/', TemplateView.as_view(template_name="checkout/error.html")),
	)

urlpatterns += patterns('',
    url(r'^order/(?P<pk>\d+)/$', login_required(OrderUpdate.as_view()), name='order_details'),
)



