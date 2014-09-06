# -*- coding: utf-8 -*-
#Copyright © Marina Gerace. All rights reserved
from django.db import models
import decimal

class CartItem(models.Model):
    """
    Item that can be added or removed from the cart.
    Every item is associated with an ingredient.
    """

    cart_id = models.CharField(max_length=50)
    date_added = models.DateTimeField(auto_now_add=True)
    ingredient = models.ForeignKey('burgers.Ingredient', unique=False)
    slug = models.SlugField(blank=True)

    class Meta:
        db_table = 'cart_items'
        ordering = ['date_added']

    def __unicode__(self):
        return self.ingredient.name

    @property
    def name(self):
        return self.ingredient.slug

    @property
    def price(self):
        return self.ingredient.price

    def get_absolute_url(self):
        return self.ingredient.get_absolute_url()

    def save(self, *args, **kwargs):
        self.slug = self.ingredient.slug
        super(CartItem, self).save(*args, **kwargs)


