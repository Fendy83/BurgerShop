# -*- coding: utf-8 -*-
#Copyright © Marina Gerace. All rights reserved
from django.contrib import admin
from models import Ingredient, Burger

class IngredientAdmin(admin.ModelAdmin):
    """
    Ingredient admin class
    """
    list_display = ('name', 'price')
    list_display_links = ('name','price')
    list_per_page = 50
    ordering = ['name']
    search_fields = ['name']

    fieldsets = (
        (None,               {'fields': (('name', 'price', 'image'), )}),
    )

admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Burger)
