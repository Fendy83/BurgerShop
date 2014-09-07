# -*- coding: utf-8 -*-
#Copyright © Marina Gerace. All rights reserved
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core import urlresolvers
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext as _
from django import forms
from django.views.generic.edit import UpdateView
from cart.models import Cart, CART_ID_SESSION_KEY
from forms import OrderForm
import decimal, datetime
from utils import create_order_list, create_order
from models import Order, order_status
from django.contrib.auth.decorators import login_required


class OrderUpdate(UpdateView):
    """
    Shows single order to the administrator and allows him to modify the status
    """
    model = Order
    fields = ['status', 'time', 'name', 'surname', 'email', 'phone', 'delivery_address', 'delivery_zip', 'comment', 'order_total_amount']

    def form_valid(self, form):
        form.save()
        success_url = urlresolvers.reverse('success')
        return HttpResponseRedirect(success_url)

    def form_invalid(self, form):
        error_url = urlresolvers.reverse('success')
        return HttpResponseRedirect(error_url)

    def get_context_data(self, **kwargs):
        context = super(OrderUpdate, self).get_context_data(**kwargs)
        context['burgers'] = self.object.orderarticle_set.all()
        return context



def order(request):
    """
    Shows to the user the checkout form and if he clicks on the 'Order' button,
    creates the order
    """
    #if cart is empty, return to homepage
    cart = ''
    cart_url = urlresolvers.reverse('show_ingredients')
    cart_id = request.session.get(CART_ID_SESSION_KEY, '')
    if not cart_id:
        return HttpResponseRedirect(cart_url)

    carts = Cart.objects.filter(cart_id=cart_id)
    if carts.count() > 0:
        cart = carts[0]
        if cart.is_empty(request):
            return HttpResponseRedirect(cart_url)


    cart_subtotal = request.session.get('cart_subtotal','')
    delivery_cost = request.session.get('delivery_cost','2.00')
    total_amount = request.session.get('total_amount','')
    if not total_amount:
        total_amount = decimal.Decimal(delivery_cost) + decimal.Decimal(cart_subtotal)

    if request.method == 'POST':
        postdata = request.POST.copy()
        form = OrderForm(postdata)
        if form.is_valid():

            # create order
            order_instance = create_order(form, total_amount, delivery_cost, cart_subtotal)

            #add order item in the order object
            create_order_list(cart, request, order_instance)

            # show the page for the order done
            order_done_url = urlresolvers.reverse('order_done')
            return HttpResponseRedirect(order_done_url)

    else:
        form = OrderForm()

    template_name='checkout/order.html'

    return render_to_response(template_name, locals(), context_instance=RequestContext(request))

def order_done(request):
    """
    Shows a message to the user when the order is successfully completed
    """

    # empty the user cart
    cart_id = request.session.get(CART_ID_SESSION_KEY, '')
    carts = Cart.objects.filter(cart_id=cart_id)
    cart = ''
    if carts.count() > 0:
        cart = carts[0]
    if cart.is_empty(request):
        cart_url = urlresolvers.reverse('show_ingredients')
        return HttpResponseRedirect(cart_url)

    cart.empty_cart(request)
    del request.session['burger']
    del request.session[CART_ID_SESSION_KEY]

    template_name='checkout/order_done.html'

    return render_to_response(template_name, locals(), context_instance=RequestContext(request))

@login_required
def show_orders(request, status = None):
    """
    Shows the orders page for the administrator
    """

    #retrieve orders
    if status:
        orders_list = Order.objects.filter(status = status)
    else:
        orders_list = Order.objects.all()

    #retrieve order status list
    status_list = order_status

    url = 'http://' + request.META['HTTP_HOST']

    template_name='checkout/orders_list.html'

    return render_to_response(template_name, locals(), context_instance=RequestContext(request))

