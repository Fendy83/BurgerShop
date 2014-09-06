# -*- coding: utf-8 -*-
#Copyright © Marina Gerace. All rights reserved
from django.db import models
from django.utils.translation import ugettext_lazy as _
from filer.fields.image import FilerImageField
from django.utils.text import slugify

class Ingredient(models.Model):
    """
    Ingredient for the burger.
    User can add more than one ingredient to the burger.
    """
    name = models.CharField(_("name"), max_length=50, unique=True)
    price = models.DecimalField(_("price"), max_digits=4, decimal_places=2, help_text=_("Example: 1.00"))
    slug = models.SlugField(_("slug"), max_length=50, unique=True, blank="True")
    image = FilerImageField(null=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Ingredient, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name
