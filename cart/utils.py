# -*- coding: utf-8 -*-
#Copyright © Marina Gerace. All rights reserved
from cart.models import Cart, CART_ID_SESSION_KEY
from django.core import urlresolvers
from django.http import HttpResponseRedirect

def get_current_cart(request):
    """creates a new cart or retrieves the current one"""

    cart_id = request.session.get(CART_ID_SESSION_KEY, '')
    cart=''

    if cart_id == '':
        cart = Cart()
        cart._cart_id(request)
    else:
        carts = Cart.objects.filter(cart_id=cart_id)
        if carts.count() <= 0:
            cart = Cart()
            cart.cart_id = cart_id
            cart.save()
        else:
            cart = carts[0]

    return cart

def get_cart_for_checkout(request):
    cart = ''
    cart_url = urlresolvers.reverse('show_ingredients')
    cart_id = request.session.get(CART_ID_SESSION_KEY, '')
    carts = Cart.objects.filter(cart_id=cart_id)

    if carts.count() > 0:
        cart = carts[0]
        if cart.is_empty(request):
            return HttpResponseRedirect(cart_url)

    return cart
