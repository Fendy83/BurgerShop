# -*- coding: utf-8 -*-
#Copyright © Marina Gerace. All rights reserved
from django.conf.urls import *
from views import OrderUpdate, OrderDone, ShowOrders
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView


urlpatterns = patterns('checkout.views',
	(r'^checkout/$', 'order', {}, 'order'),
	url(r'^order_done/$', OrderDone.as_view(), name='order_done'),
	url(r'^orders/$', ShowOrders.as_view(), name='show_orders'),
    url(r'^orders/(?P<status>[-\w]+)/$', ShowOrders.as_view(), name='show_orders'),
    url(r'^success/', TemplateView.as_view(template_name="checkout/success.html"), name='success'),
    url(r'^error/', TemplateView.as_view(template_name="checkout/error.html"), name='error'),
	)

urlpatterns += patterns('',
    url(r'^order/(?P<pk>\d+)/$', login_required(OrderUpdate.as_view()), name='order_details'),
)



