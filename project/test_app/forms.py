from django import forms
from .models import Test
from subjects.models import Topic
from django.conf import settings
from tempus_dominus.widgets import DatePicker, TimePicker
import datetime

today = str(datetime.datetime.today())

class TestForm(forms.ModelForm):
	date_scheduled = forms.DateField(
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
		model = Test
		fields = ('name', 'cutoff_mark','date_scheduled', 'no_of_questions',
			'opening_time', 'closing_time', 'batch', 'max_mark')

class TopicDistributionForm(forms.Form):
	# topic = forms.ModelChoiceField(queryset=Topic.objects.all(), required=True)
	no_of_questions = forms.IntegerField(min_value=1)

	def __init__(self, request, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['topic']= forms.ModelChoiceField(
			queryset=Topic.objects.filter(
			subject__id = request.session['subject_id']
			)
		)

