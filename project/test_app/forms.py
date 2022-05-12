from django import forms
from .models import Test
from subjects.models import Topic, Subject
from batches.models import Batch
from django.conf import settings
from tempus_dominus.widgets import DatePicker, TimePicker
import datetime
from batches.utils import is_time_between

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
				'class': 'opening_time'
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
				'class': 'closing_time'
			},
		),
	)
	def __init__(self, request=None, *args, **kwargs):
		super ().__init__(*args,**kwargs)
		if request != None:
			subject = Subject.objects.get(id=request.session['subject_id'])
			self.fields['batch'].queryset = Batch.objects.filter(exam_category__subjects=subject)

	class Meta:
		model = Test
		fields = ('name', 'cutoff_mark','date_scheduled', 'no_of_questions',
			'opening_time', 'closing_time', 'batch', 'max_mark')

	def clean(self):
		cleaned_data = super().clean()
		start_time = cleaned_data.get("opening_time")
		end_time = cleaned_data.get("closing_time")
		date_scheduled = cleaned_data.get("date_scheduled")
		if end_time < start_time:
			raise forms.ValidationError("Closing time should be greater than opening time.")
		batch = cleaned_data.get("batch")
		start_time = datetime.datetime.combine(date_scheduled, start_time)
		end_time = datetime.datetime.combine(date_scheduled, end_time)
		for test_obj in Test.objects.filter(batch=batch):
			if test_obj.id != self.instance.pk:
				opening_time = datetime.datetime.combine(test_obj.date_scheduled, test_obj.opening_time)
				closing_time = datetime.datetime.combine(test_obj.date_scheduled, test_obj.closing_time)
				if is_time_between(start_time, end_time, opening_time):
					raise forms.ValidationError("These batch timings are in conflict with other timings.")
				if is_time_between(start_time, end_time, closing_time):
					raise forms.ValidationError("These batch timings are in conflict with other timings.")
				if is_time_between(opening_time, closing_time, start_time):
					raise forms.ValidationError("These batch timings are in conflict with other timings.")
				if is_time_between(opening_time, closing_time, end_time):
					raise forms.ValidationError("These batch timings are in conflict with other timings.")

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

