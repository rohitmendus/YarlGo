from django import forms
from .models import MainExam

class MainExamForm(forms.ModelForm):
	class Meta:
		model = MainExam
		fields = ('name', 'description')
		widgets = {
            'description': forms.Textarea(),
        }