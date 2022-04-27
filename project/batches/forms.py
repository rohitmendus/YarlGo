from django import forms
from .models import Batch
# from .widgets import DatePickerInput
from django.conf import settings
from tempus_dominus.widgets import DatePicker
import datetime

today = str(datetime.datetime.today())

class BatchForm(forms.ModelForm):
	opening_date = forms.DateField(
        required=True, input_formats = settings.DATE_INPUT_FORMATS,
        widget=DatePicker(
            options={
                'minDate': today,
                # Calendar and time widget formatting
                'time': 'fa fa-clock-o',
                'date': 'fa fa-calendar',
                'up': 'fa fa-arrow-up',
                'down': 'fa fa-arrow-down',
                'previous': 'fa fa-chevron-left',
                'next': 'fa fa-chevron-right',
                'today': 'fa fa-calendar-check-o',
                'clear': 'fa fa-delete',
                'close': 'fa fa-times',
            },
            attrs={
                'append': 'fa fa-calendar',
            }
        ),
    )
	closing_date = forms.DateField(
        required=True, input_formats = settings.DATE_INPUT_FORMATS,
        widget=DatePicker(
            options={
                'minDate': today,
                # Calendar and time widget formatting
                'time': 'fa fa-clock-o',
                'date': 'fa fa-calendar',
                'up': 'fa fa-arrow-up',
                'down': 'fa fa-arrow-down',
                'previous': 'fa fa-chevron-left',
                'next': 'fa fa-chevron-right',
                'today': 'fa fa-calendar-check-o',
                'clear': 'fa fa-delete',
                'close': 'fa fa-times'
            },
            attrs={
                'append': 'fa fa-calendar',
            }
        ),
    )
	class Meta:
		model = Batch
		fields = ('name', 'opening_date', 'closing_date', 'exam_category', 'students')