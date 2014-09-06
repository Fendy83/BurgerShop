# -*- coding: utf-8 -*-
#Copyright © Marina Gerace. All rights reserved
from django import forms
from django.utils.translation import ugettext_lazy as _
from models import CartItem

class ProductAddToCartForm(forms.ModelForm):
    """
    form used to add ingredients in the cart
    """

    product_slug = forms.CharField(required=False, widget=forms.HiddenInput())

    class Meta:
        model = CartItem

    # override the default __init__ so we can set the request
    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        super(ProductAddToCartForm, self).__init__(*args, **kwargs)

    # custom validation to check for cookies
    def clean(self):
        cleaned_data = super(ProductAddToCartForm, self).clean()
        if self.request:
            if not self.request.session.test_cookie_worked():
                raise forms.ValidationError(_("Cookies must be enabled."))
        return self.cleaned_data
