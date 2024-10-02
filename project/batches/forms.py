from django import forms
from .models import Batch, BatchTiming
from django.contrib.auth.models import User
from django.conf import settings
from tempus_dominus.widgets import DatePicker, TimePicker
import datetime
from .utils import is_time_between

today = str(datetime.datetime.today())

class CustomMultipleWidget(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return f'{obj.first_name} {obj.last_name} - {obj.email}'

class BatchForm(forms.ModelForm):
    students = CustomMultipleWidget(
        queryset=User.objects.filter(roles__name="student"),
        widget=forms.CheckboxSelectMultiple(
            attrs={'class':'form-check-input'}),
        required=True)
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
                'class': 'opening_date'
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
                'class': 'closing_date'
            }
        ),
    )
    class Meta:
        model = Batch
        fields = ('name', 'opening_date', 'closing_date', 'exam_category', 'students')

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("opening_date")
        end_date = cleaned_data.get("closing_date")
        if end_date < start_date:
            raise forms.ValidationError("Closing date should be greater than opening date.")

class BatchTimingForm(forms.ModelForm):
    opening_time = forms.TimeField(
        input_formats = settings.TIME_INPUT_FORMATS,
        widget=TimePicker(
            options={
                'enabledHours': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 0],
                'defaultDate': '1970-01-01T14:56:00',
                'format': 'hh:mm A'
            },
            attrs={
                'input_toggle': True,
                'input_group': True,
                'append': 'fa-solid fa-clock',
                'icon_toggle': True,
                'class': 'opening_time'
            },
        ),
    )
    closing_time = forms.TimeField(
        input_formats = settings.TIME_INPUT_FORMATS,
        widget=TimePicker(
            options={
                'enabledHours': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 0],
                'defaultDate': '1970-01-01T14:56:00',
                'format': 'hh:mm A'
            },
            attrs={
                'input_toggle': True,
                'input_group': True,
                'append': 'fa-solid fa-clock',
                'icon_toggle': True,
                'class': 'closing_time'
            },
        ),
    )
    class Meta:
        model = BatchTiming
        fields = ('batch', 'subject', 'opening_time', 'closing_time')

    def clean(self):
        cleaned_data = super().clean()
        # Timing conflicts
        start_time = cleaned_data.get("opening_time")
        end_time = cleaned_data.get("closing_time")
        if end_time < start_time:
            raise forms.ValidationError("Closing time should be greater than opening time.")
        batch = cleaned_data.get("batch")
        for batch_obj in BatchTiming.objects.filter(batch=batch):
            if batch_obj.id != self.instance.pk:
                if is_time_between(start_time, end_time, batch_obj.opening_time):
                    raise forms.ValidationError("These batch timings are in conflict with other timings.")
                if is_time_between(start_time, end_time, batch_obj.closing_time):
                    raise forms.ValidationError("These batch timings are in conflict with other timings.")
                if is_time_between(batch_obj.opening_time, batch_obj.closing_time, start_time):
                    raise forms.ValidationError("These batch timings are in conflict with other timings.")
                if is_time_between(batch_obj.opening_time, batch_obj.closing_time, end_time):
                    raise forms.ValidationError("These batch timings are in conflict with other timings.")

        batch = cleaned_data.get('batch')
        subject = cleaned_data.get('subject')
        if not subject.exam_categories.filter(id=batch.exam_category.id).exists():
            raise forms.ValidationError("The subject is not alloted for the batch.")