# -*- coding: utf-8 -*-
#Copyright © Marina Gerace. All rights reserved
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core import urlresolvers
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext as _
from django import forms
from django.views.generic.edit import UpdateView
from django.views.generic import TemplateView, View, CreateView
from cart.models import Cart, CART_ID_SESSION_KEY
from cart.utils import get_cart_for_checkout
from forms import OrderForm
import decimal, datetime
from utils import create_order_list, create_order
from models import Order, order_status
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class OrderUpdate(UpdateView):
    """
    Shows single order to the administrator and allows him to modify the status
    """
    model = Order
    fields = ['status', 'time', 'name', 'surname', 'email', 'phone', 'delivery_address',
              'delivery_zip', 'comment', 'order_total_amount']

    def form_valid(self, form):
        form.save()
        success_url = urlresolvers.reverse('success')
        return HttpResponseRedirect(success_url)

    def form_invalid(self, form):
        error_url = urlresolvers.reverse('error')
        return HttpResponseRedirect(error_url)

    def get_context_data(self, **kwargs):
        context = super(OrderUpdate, self).get_context_data(**kwargs)
        context['burgers'] = self.object.orderarticle_set.all()
        return context

class OrderCreate(CreateView):
    """
    Shows to the user the checkout form and if he clicks on the 'Order' button,
    creates the order
    """
    template_name='checkout/order.html'
    success_url = urlresolvers.reverse_lazy('order_done')
    model = Order
    form_class = OrderForm

    def get_context_data(self, **kwargs):
        context = super(OrderCreate, self).get_context_data(**kwargs)
        #if cart is empty, return to homepage
        cart = get_cart_for_checkout(self.request)
        if cart.is_empty():
            cart_url = urlresolvers.reverse('show_ingredients')
            return HttpResponseRedirect(cart_url)
        else:
            context['cart'] = cart

        context['cart_subtotal'] = self.request.session.get('cart_subtotal','')
        context['delivery_cost'] = self.request.session.get('delivery_cost','2.00')
        context['total_amount'] = self.request.session.get('total_amount','')

        if context['total_amount'] == '':
            context['total_amount'] = decimal.Decimal(context['delivery_cost']) + decimal.Decimal(context['cart_subtotal'])

        return context

    def form_valid(self, form):
        cart = get_cart_for_checkout(self.request)
        if cart.is_empty():
            cart_url = urlresolvers.reverse('show_ingredients')
            return HttpResponseRedirect(cart_url)

        cart_subtotal = self.request.session.get('cart_subtotal','')
        delivery_cost = self.request.session.get('delivery_cost','2.00')
        total_amount = self.request.session.get('total_amount','')

        if not total_amount:
            total_amount = decimal.Decimal(delivery_cost) + decimal.Decimal(cart_subtotal)

        # create order
        order_instance = create_order(form, total_amount, delivery_cost, cart_subtotal)

        #add order item in the order object
        create_order_list(cart, self.request, order_instance)

        return super(OrderCreate, self).form_valid(form)


class OrderDone(TemplateView):
    """Shows a success message to the user and empty the cart"""
    template_name = 'checkout/order_done.html'

    def get(self, request, *args, **kwargs):
        # empty the user cart
        cart = get_cart_for_checkout(request)
        cart.delete()

        del request.session['burger']
        del request.session[CART_ID_SESSION_KEY]

        return render_to_response(self.template_name, locals(), context_instance=RequestContext(request))

class ShowOrders(TemplateView):
    template_name = 'checkout/orders_list.html'

    @method_decorator(login_required)
    def get(self, request, status = None):
        #retrieve orders
        if status:
            orders_list = Order.objects.filter(status = status)
        else:
            orders_list = Order.objects.all()

        #retrieve order status list
        status_list = order_status
        url = 'http://' + request.META['HTTP_HOST']

        return render_to_response(self.template_name, locals(), context_instance=RequestContext(request))
