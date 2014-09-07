# -*- coding: utf-8 -*-
#Copyright © Marina Gerace. All rights reserved
from models import Burger
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

def get_current_burger(request, burger_name=''):
    if burger_name == '':
        burger_name = request.session.get('burger', '')
    burgers = Burger.objects.filter(name=burger_name)

    if burgers.count() > 0:
        burger = burgers[0]
    else:
        initial_page = reverse('create_burger')
        return HttpResponseRedirect(initial_page)

    return burger