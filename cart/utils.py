# -*- coding: utf-8 -*-
#Copyright © Marina Gerace. All rights reserved
from models import CartItem
from burgers.models import Ingredient, Burger
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
import decimal
import random
from django.contrib.sessions.models import Session
from django.core.urlresolvers import reverse

CART_ID_SESSION_KEY = 'cart_id'


def _cart_id(request):
    """
    get the current user's cart id, sets new one if blank
    """
    if request.session.get(CART_ID_SESSION_KEY, '') == '' :
        request.session[CART_ID_SESSION_KEY] = _generate_cart_id()
    return request.session[CART_ID_SESSION_KEY]

def _generate_cart_id():
    """
    create a cart id
    """
    cart_id = ''
    characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890!@#$%^&*()'
    cart_id_length = 50
    for y in range(cart_id_length):
        cart_id += characters[random.randint(0, len(characters) - 1)]

    return cart_id

def get_cart_items(request):
    """
    return all items from the current user's cart
    """
    return CartItem.objects.filter(cart_id=_cart_id(request))

def add_to_cart(request):
    """
    add an item to the cart
    """
    postdata = request.POST.copy()

    #retrieve the burger
    burger_name = request.session.get('burger', '')
    if burger_name == '':
        initial_page = reverse('create_burger')
        return HttpResponseRedirect(initial_page)

    burgers = Burger.objects.filter(name=burger_name)
    if burgers.count() > 0:
        burger = burgers[0]

        ingredient_slug = postdata.get('product_slug', '')

        if ingredient_slug:
            # fetch the product or return a missing page error
            i = get_object_or_404(Ingredient, slug=ingredient_slug)

            #connect ingredient to the burger
            burger.ingredients.add(i)

            # get products in cart
            cart_products = get_cart_items(request)
            product_in_cart = False

            # check to see if item is already in cart
            for cart_item in cart_products:
                if cart_item.burger.id == burger.id:
                    product_in_cart = True

            if not product_in_cart:
                # create and save a new cart item
                ci = CartItem()
                ci.burger = burger
                ci.cart_id = _cart_id(request)
                ci.save()


def cart_item_count(request):
    """
    return number of items in the cart
    """
    return CartItem.objects.filter(cart_id=_cart_id(request)).count()


def get_single_item(request, item_id):
    return get_object_or_404(CartItem, id=item_id, cart_id=_cart_id(request))

# remove a single item from cart
def remove_from_cart(request):
    postdata = request.POST.copy()

    if "item_id" in postdata:
        item_id = postdata['item_id']
        cart_item = get_single_item(request, item_id)
        if cart_item:
            cart_item.delete()
            cart_item.burger.delete()

    if cart_item_count(request) == 0:
        return HttpResponseRedirect(reverse(viewname='create_burger'))


# gets the total cost for the cart
def cart_subtotal(request):
    cart_total = decimal.Decimal('0.00')
    cart_products = get_cart_items(request)
    for cart_item in cart_products:
        cart_total += decimal.Decimal(cart_item.burger.price)
        for ingredient in cart_item.burger.ingredients.all():
            cart_total += decimal.Decimal(ingredient.price)
    return cart_total

def is_empty(request):
    return cart_item_count(request) == 0

def empty_cart(request):
    """
    Empty the cart
    """
    user_cart = get_cart_items(request)
    user_cart.delete()







