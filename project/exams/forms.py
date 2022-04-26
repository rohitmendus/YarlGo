from django import forms
from .models import MainExam, ExamCategory

class MainExamForm(forms.ModelForm):
	class Meta:
		model = MainExam
		fields = ('name', 'description')
		widgets = {
			'description': forms.Textarea(),
		}

class ExamCategoryForm(forms.ModelForm):
	class Meta:
		model = ExamCategory
		fields = ('name', 'description', 'main_exam')
		widgets = {
			'description': forms.Textarea(),
		}