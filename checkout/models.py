# -*- coding: utf-8 -*-
#Copyright © Marina Gerace. All rights reserved
from django.db import models
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from burgers.models import Ingredient
import decimal

order_status = [
    ('ordered', _('ordered')),
    ('in_progress', _('in progress')),
    ('on_the_road', _('on the road')),
    ('delivered', _('delivered')),
]

class BaseOrderInfo(models.Model):
    """
    Contact information and address of the user
    """
    class Meta:
        abstract = True

    name = models.CharField(_("name"), max_length=200)
    surname = models.CharField(_("surname"), max_length=200)
    email = models.EmailField(_("email"), max_length=50)
    phone = models.CharField(_("phone"), max_length=200)

    delivery_address = models.CharField(_("delivery address"), max_length=50)
    delivery_zip = models.CharField(_("delivery zip"), max_length=10)

class Order(BaseOrderInfo) :
    """
    Information about the order
    """
    time = models.TimeField(_("Time"))
    comment = models.TextField(_('Comment'), max_length=255, blank=True, null=True)
    status = models.CharField(_("status"), max_length=200, choices=order_status)
    order_total_amount = models.DecimalField(_("Tot."), max_digits=8, decimal_places=2)
    delivery_cost = models.DecimalField(max_digits=8, decimal_places=2, default=2.00)
    cart_subtotal = models.DecimalField(max_digits=8, decimal_places=2)
    created_at = models.DateTimeField(_("created_at"), editable=True, db_index=True)

    class Meta:
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')
        ordering = ['-pk']

    def __unicode__(self):
        return 'Order for ' + self.name + ' ' + self.surname + ' ' + self.time

    @property
    def total(self):
        total = decimal.Decimal('0.00')
        order_items = OrderArticle.objects.filter(order=self)
        for item in order_items:
            total += item.total
        return total

    @models.permalink
    def get_absolute_url(self):
        return reverse('order_details', kwargs={'pk': self.pk})

class OrderArticle(models.Model):
    """
    Single product in the order (ingredient)
    """
    ingredient = models.ForeignKey(Ingredient, verbose_name=_("ingredient"))
    order = models.ForeignKey(Order)

    @property
    def price(self):
        return self.ingredient.price

    @property
    def name(self):
        return self.ingredient.name

    def __unicode__(self):
        return self.ingredient.name

