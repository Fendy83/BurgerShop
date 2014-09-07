# -*- coding: utf-8 -*-
#Copyright © Marina Gerace. All rights reserved
from django.shortcuts import render_to_response
from django.template import RequestContext
from models import Ingredient, Burger
from django.utils.translation import ugettext as _
from cart.forms import ProductAddToCartForm
from cart.models import CartItem, Cart, CART_ID_SESSION_KEY
from django.views.generic.edit import CreateView
from django.core.urlresolvers import reverse_lazy, reverse
from django.http import HttpResponseRedirect

class BurgerCreate(CreateView):
    template_name = "burgers/burger.html"
    model = Burger
    fields = ['name']
    success_url = reverse_lazy('show_ingredients')

    def form_valid(self, form):
        #save burger name in session
        self.request.session['burger'] = form.instance.name
        return super(BurgerCreate, self).form_valid(form)

def show_ingredients(request):

    """
    show burger ingredients and cart
    """

    ingredients = Ingredient.objects.all()
    burger_name = request.session.get('burger', '')
    burgers = Burger.objects.filter(name=burger_name)
    if burgers.count() > 0:
        burger = burgers[0]
    else:
        initial_page = reverse('create_burger')
        return HttpResponseRedirect(initial_page)

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

    cart_items = cart.get_cart_items(request)

    #for adding the ingredient to the burger and show it in the cart
    form = ProductAddToCartForm(request=request)

    # set the test cookie on our first GET request
    request.session.set_test_cookie()

    if request.method == 'POST':
        postdata = request.POST.copy()

        # remove the burger from the cart
        if postdata['submit'] == _('Remove'):
            cart.remove_from_cart(request)
            burger_name = request.session.get('burger', '')

            # remove the ingredient from the burger
        if postdata['submit'] == _('Delete'):
            burger.remove_ingredient(postdata['ingredient'])

        # update the specific burger
        if postdata['submit'] == _('Update'):
            request.session['burger'] = postdata['burger']
            burger_name = postdata['burger']
            burgers = Burger.objects.filter(name=burger_name)
            if burgers.count() > 0:
                burger = burgers[0]

            # add the ingredient to the cart
        if postdata['submit'] == _("Add"):
            form = ProductAddToCartForm(request, postdata)

            if form.is_valid():
                cart.add_to_cart(request)

                # if test cookie worked, get rid of it
                if request.session.test_cookie_worked():
                    request.session.delete_test_cookie()

    # retrieve total amount of the order
    if cart:
        order_subtotal = cart.cart_subtotal(request)
    else:
        order_subtotal = 0
    request.session['cart_subtotal'] = str(order_subtotal)

    template_name="burgers/home.html"

    return render_to_response(template_name, locals(),context_instance=RequestContext(request))


