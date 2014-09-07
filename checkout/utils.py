# -*- coding: utf-8 -*-
#Copyright © Marina Gerace. All rights reserved
from cart.models import Cart, CART_ID_SESSION_KEY
from models import OrderArticle
import datetime

def create_order(form, total_amount, delivery_cost, cart_subtotal):
    """creates an order object"""
    order_instance = form.save(commit=False)
    order_instance.created_at = datetime.datetime.now()
    order_instance.status = 'ordered'
    order_instance.order_total_amount = total_amount
    order_instance.delivery_cost = delivery_cost
    order_instance.cart_subtotal = cart_subtotal
    order_instance.save()

    return order_instance

def create_order_list(cart, request, order_instance) :
    """For each burger in the cart, create an article in the order"""
    cart_items = cart.get_cart_items(request)
    for ci in cart_items:
        oi = OrderArticle()
        oi.order = order_instance
        oi.burger = ci.burger
        oi.save()

    results = {'order_number': order_instance.id,'message':''}

    return results