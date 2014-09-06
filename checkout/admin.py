# -*- coding: utf-8 -*-
#Copyright © Marina Gerace. All rights reserved
from django.contrib import admin
from models import Order, OrderArticle

class OrderArticleAdmin(admin.StackedInline) :
    """
    Single item in the order (ingredient)
    """
    model = OrderArticle
    extra = 0

    def __unicode__(self):
        return "item"

class OrderAdmin(admin.ModelAdmin) :
    """
    Delivery orders
    """

    list_display = ('surname','time')
    list_display_links = ('surname', 'time')
    list_filter = ('status',)
    list_per_page = 15

    fieldsets = [
        ('Basic',            {'fields' : [('created_at','time', 'status'),
                                          ('name', 'surname', 'email'),
                                          ('delivery_address', 'delivery_zip', 'phone')]}),
        ('Order amount',     {'fields' : [('order_total_amount', 'delivery_cost', 'cart_subtotal', ),
                                          'comment']}),

        ]
    inlines = [OrderArticleAdmin]

admin.site.register(Order, OrderAdmin)
