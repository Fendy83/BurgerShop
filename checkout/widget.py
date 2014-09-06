# -*- coding: utf-8 -*-
#Copyright © Marina Gerace. All rights reserved
from django.forms.widgets import Select, MultiWidget, DateInput, TextInput
from time import strftime
import constants
from django.utils.translation import ugettext_lazy as _


class JqSplitTimeWidget(MultiWidget):
    """
    Custom widget for the time (hours : minutes)
    """

    def __init__(self, attrs=None, date_format=None, time_format=None):
        time_class = attrs['time_class']
        del attrs['time_class']

        time_attrs = attrs.copy()
        time_attrs['class'] = time_class
        widgets = (Select(attrs=time_attrs, choices = constants.hours_options),
                   Select(attrs=time_attrs, choices = constants.minutes_options))

        super(JqSplitTimeWidget, self).__init__(widgets, attrs)


    def decompress(self, value):
        if value:
            hour = strftime("%H", value.timetuple())
            minute = strftime("%M", value.timetuple())

            return (hour, minute)
        else:
            return (None, None)

    def format_output(self, rendered_widgets):
        """
        Given a list of rendered widgets (as strings), it inserts an HTML
        linebreak between them.

        Returns a Unicode string representing the HTML for the whole lot.
        """
        time_label = _("* Time")

        widget_label = u"<label for='id_date_0' class='col-md-2 col-md-offset-3 control-label'>%s</label><div class='col-md-4'> %s<label class='text-center col-md-1'> : </label>%s</div>"
        return widget_label % (time_label, rendered_widgets[0], rendered_widgets[1])





