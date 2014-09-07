# -*- coding: utf-8 -*-
#Copyright © Marina Gerace. All rights reserved
from django.db import models
import decimal
import random
from django.contrib.sessions.models import Session
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from burgers.models import Burger
from django.http import HttpResponseRedirect
from burgers.models import Ingredient

CART_ID_SESSION_KEY = 'cart_id'

def _generate_cart_id():
    """create a cart id"""
    cart_id = ''
    characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890!@#$%^&*()'
    cart_id_length = 50
    for y in range(cart_id_length):
        cart_id += characters[random.randint(0, len(characters) - 1)]

    return cart_id

class Cart(models.Model):
    cart_id = models.CharField(max_length=50, default=_generate_cart_id())

    def __unicode__(self):
        return self.cart_id

    def _cart_id(self, request):
        """get the current user's cart id, sets new one if blank"""
        if request.session.get(CART_ID_SESSION_KEY, '') == '' :
            self.cart_id = _generate_cart_id()
            request.session[CART_ID_SESSION_KEY] = self.cart_id
        return request.session[CART_ID_SESSION_KEY]

    def add_to_cart(self, request):
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
                cart_products = self.cartitem_set.all()
                product_in_cart = False

                # check to see if item is already in cart
                for cart_item in cart_products:
                    if cart_item.burger.id == burger.id:
                        product_in_cart = True

                if not product_in_cart:
                    # create and save a new cart item
                    ci = CartItem()
                    ci.burger = burger
                    ci.cart = self
                    ci.save()


    def cart_item_count(self):
        """return number of items in the cart"""
        return self.cartitem_set.count()


    def get_single_item(self, request, item_id):
        return get_object_or_404(CartItem, id=item_id, cart=self)

    def remove_from_cart(self, request):
        """remove a single item from cart"""
        postdata = request.POST.copy()

        if "item_id" in postdata:
            item_id = postdata['item_id']
            cart_item = self.get_single_item(request, item_id)
            if cart_item:
                cart_item.delete()
                cart_item.burger.delete()

        #if cart is not empty sets another burger as current burger
        if self.cart_item_count() == 0:
            return HttpResponseRedirect(reverse(viewname='create_burger'))
        else:
            current_burger = CartItem.objects.all()[0]
            request.session['burger'] = current_burger.burger.name

    # gets the total cost for the cart
    def cart_subtotal(self, request):
        cart_total = decimal.Decimal('0.00')
        cart_products = self.cartitem_set.all()
        for cart_item in cart_products:
            cart_total += decimal.Decimal(cart_item.burger.price)
            for ingredient in cart_item.burger.ingredients.all():
                cart_total += decimal.Decimal(ingredient.price)
        return cart_total

    def is_empty(self):
        return self.cart_item_count() == 0

class CartItem(models.Model):
    """
    Item that can be added or removed from the cart.
    Every item is associated with an ingredient.
    """

    cart = models.ForeignKey(Cart)
    date_added = models.DateTimeField(auto_now_add=True)
    burger = models.ForeignKey('burgers.Burger')
    slug = models.SlugField(blank=True)

    class Meta:
        db_table = 'cart_items'
        ordering = ['date_added']

    def __unicode__(self):
        return self.burger.name

    def get_absolute_url(self):
        return self.burger.get_absolute_url()

    def save(self, *args, **kwargs):
        self.slug = self.burger.slug
        super(CartItem, self).save(*args, **kwargs)


