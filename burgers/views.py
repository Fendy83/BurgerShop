# -*- coding: utf-8 -*-
#Copyright © Marina Gerace. All rights reserved
from django.shortcuts import render_to_response
from django.template import RequestContext
from models import Ingredient, Burger
from django.utils.translation import ugettext as _
from cart.forms import ProductAddToCartForm
from django.views.generic.edit import CreateView
from django.views.generic import View
from django.core.urlresolvers import reverse_lazy
from burgers.utils import get_current_burger
from cart.utils import get_current_cart

class BurgerCreate(CreateView):
    template_name = "burgers/burger.html"
    model = Burger
    fields = ['name']
    success_url = reverse_lazy('show_ingredients')

    def form_valid(self, form):
        #save burger name in session
        self.request.session['burger'] = form.instance.name
        return super(BurgerCreate, self).form_valid(form)

class ShowIngredients(View):
    """show burger ingredients and cart"""
    template_name="burgers/home.html"

    def get(self, request):
        ingredients = Ingredient.objects.all()
        burger = get_current_burger(request)
        cart = get_current_cart(request)
        cart_items = cart.get_cart_items(request)

        #for adding the ingredient to the burger and show it in the cart
        form = ProductAddToCartForm(request=request)

        # set the test cookie on our first GET request
        request.session.set_test_cookie()
        # retrieve total amount of the order
        order_subtotal = cart.cart_subtotal(request)
        request.session['cart_subtotal'] = str(order_subtotal)

        return render_to_response(self.template_name, locals(),context_instance=RequestContext(request))

    def post(self, request):
        ingredients = Ingredient.objects.all()
        burger = get_current_burger(request)
        cart = get_current_cart(request)
        cart_items = cart.get_cart_items(request)

        #for adding the ingredient to the burger and show it in the cart
        form = ProductAddToCartForm(request=request)

        # set the test cookie on our first GET request
        request.session.set_test_cookie()

        # retrieve total amount of the order
        order_subtotal = cart.cart_subtotal(request)
        request.session['cart_subtotal'] = str(order_subtotal)

        postdata = request.POST.copy()

        # remove the burger from the cart
        if postdata['submit'] == _('Remove'):
            cart.remove_from_cart(request)
            burger = get_current_burger(request)

            # remove the ingredient from the burger
        if postdata['submit'] == _('Delete'):
            burger.remove_ingredient(postdata['ingredient'])

        # update the specific burger
        if postdata['submit'] == _('Update'):
            request.session['burger'] = postdata['burger']
            burger = get_current_burger(request, postdata['burger'])

            # add the ingredient to the cart
        if postdata['submit'] == _("Add"):
            form = ProductAddToCartForm(request, postdata)

            if form.is_valid():
                cart.add_to_cart(request)

                # if test cookie worked, get rid of it
                if request.session.test_cookie_worked():
                    request.session.delete_test_cookie()

        return render_to_response(self.template_name, locals(),context_instance=RequestContext(request))
