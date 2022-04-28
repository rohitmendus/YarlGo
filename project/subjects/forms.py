from django import forms
from .models import Subject, Topic

class SubjectForm(forms.ModelForm):
	class Meta:
		model = Subject
		fields = ('name', 'description')
		widgets = {
			'description': forms.Textarea(),
		}

class TopicForm(forms.ModelForm):
	class Meta:
		model = Topic
		fields = ('name', 'description')
		widgets = {
			'description': forms.Textarea(),
		}