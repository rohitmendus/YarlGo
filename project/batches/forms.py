from django import forms
from .models import Batch, BatchTiming
from django.conf import settings
from tempus_dominus.widgets import DatePicker, TimePicker
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

class BatchTimingForm(forms.ModelForm):
    opening_time = forms.TimeField(
        input_formats = settings.TIME_INPUT_FORMATS,
        widget=TimePicker(
            options={
                'enabledHours': [9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
                'defaultDate': '1970-01-01T14:56:00',
                'format': 'hh:mm A'
            },
            attrs={
                'input_toggle': True,
                'input_group': True,
                'append': 'fa-solid fa-clock',
                'icon_toggle': True,
            },
        ),
    )
    closing_time = forms.TimeField(
        input_formats = settings.TIME_INPUT_FORMATS,
        widget=TimePicker(
            options={
                'enabledHours': [9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
                'defaultDate': '1970-01-01T14:56:00',
                'format': 'hh:mm A'
            },
            attrs={
                'input_toggle': True,
                'input_group': True,
                'append': 'fa-solid fa-clock',
                'icon_toggle': True,
            },
        ),
    )
    class Meta:
        model = BatchTiming
        fields = ('batch', 'subject', 'opening_time', 'closing_time')
