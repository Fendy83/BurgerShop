# -*- coding: utf-8 -*-
#Copyright © Marina Gerace. All rights reserved
from django.shortcuts import render_to_response
from django.template import RequestContext
from models import Ingredient
from django.utils.translation import ugettext as _
from cart.forms import ProductAddToCartForm
from cart.utils import add_to_cart, get_cart_items, remove_from_cart, cart_subtotal

def show_ingredients(request):

    """
    show burger ingredients and cart
    """

    ingredients = Ingredient.objects.all()
    cart_items = get_cart_items(request)

    #for adding the ingredient to the burger and show it in the cart
    form = ProductAddToCartForm(request=request)

    # set the test cookie on our first GET request
    request.session.set_test_cookie()

    if request.method == 'POST':
        postdata = request.POST.copy()

        # remove the ingredient from the cart
        if postdata['submit'] == _('Remove'):
            remove_from_cart(request)

        # add the ingredient to the cart
        if postdata['submit'] == _("Add"):
            form = ProductAddToCartForm(request, postdata)

            if form.is_valid():
                add_to_cart(request)

                # if test cookie worked, get rid of it
                if request.session.test_cookie_worked():
                    request.session.delete_test_cookie()

    # retrieve total amount of the order
    order_subtotal = cart_subtotal(request)
    request.session['cart_subtotal'] = str(order_subtotal)

    template_name="burgers/home.html"

    return render_to_response(template_name, locals(),context_instance=RequestContext(request))
