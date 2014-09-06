# -*- coding: utf-8 -*-
#Copyright © Marina Gerace. All rights reserved
from time import strptime, strftime
from django import forms
import datetime, re
from django.forms import fields
from widget import JqSplitTimeWidget
from django.utils.translation import ugettext_lazy as _
from django.core.validators import ValidationError
import constants


class PhoneField(forms.CharField) :
    """
    Phone field for forms
    """
    default_error_messages = {
    'not_a_phone_number' : _(u'input a valid phone number'),
    'required' : _(u'This field is required.')
    }

    def __init__(self, *args, **kwargs):
        super(PhoneField, self).__init__(*args, **kwargs)
        self.label = _("Phone")

    def to_python(self, value) :
        if not value:
            return []
        return value

    def validate(self, value) :

        # allow phone numbers that starts with '+' and having spaces, '-' and '.' in the middle
        if value != [] :
            number = re.match(r'^\+*\(?([0-9]*)\)?[-. ]?([0-9]*)[-. ]?([0-9]*)[-. ]?([0-9]*)$', value)

        else:
            raise ValidationError(self.error_messages['required'])

        if (len(value) >= 8 and number):
            return number
        else:
            raise ValidationError(self.error_messages['not_a_phone_number'])


class JqSplitTimeField(fields.MultiValueField):
    """
    Custom widget for time (hours : minutes)
    """
    widget = JqSplitTimeWidget

    def __init__(self, *args, **kwargs):
        """
        Have to pass a list of field types to the constructor, else we
        won't get any data to our compress method.
        """
        all_fields = (
            fields.ChoiceField(choices = constants.hours_options ),
            fields.ChoiceField(choices = constants.minutes_options)
        )
        super(JqSplitTimeField, self).__init__(all_fields, *args, **kwargs)
        self.label = ""



    def compress(self, data_list):
        """
        Takes the values from the MultiWidget and passes them as a
        list to this function. This function needs to compress the
        list into a single object to save.
        """

        if data_list:
            #check if the form filling is complete
            if not (data_list[0] and data_list[1]):
                raise forms.ValidationError(_("Field is missing data."))

            input_time = strptime("%s:%s"%(data_list[0], data_list[1]), "%H:%M")
            datetime_string = "%s" % (strftime('%H:%M', input_time))
            return datetime_string
        return None




