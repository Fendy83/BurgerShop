# -*- coding: utf-8 -*-
#Copyright © Marina Gerace. All rights reserved
from django import forms
from models import Order
import widget, fields

class OrderForm(forms.ModelForm) :
    """form for the order"""

    time = fields.JqSplitTimeField(widget=widget.JqSplitTimeWidget(attrs={'time_class':'timepicker'}))
    phone = fields.PhoneField()

    class Meta:
        model = Order
        exclude = ['created_at', 'status', 'order_total_amount', 'delivery_cost', 'cart_subtotal']
