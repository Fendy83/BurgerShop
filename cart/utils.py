# -*- coding: utf-8 -*-
#Copyright © Marina Gerace. All rights reserved
from cart.models import Cart, CART_ID_SESSION_KEY
from django.shortcuts import get_object_or_404

def get_current_cart(request):
    """creates a new cart or retrieves the current one"""
    cart_id = request.session.get(CART_ID_SESSION_KEY, '')

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
    cart_id = request.session.get(CART_ID_SESSION_KEY, '')
    cart = get_object_or_404(Cart, cart_id=cart_id)

    return cart
