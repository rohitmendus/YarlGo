from django import forms
from .models import MainExam, ExamCategory
from subjects.models import Subject

class MainExamForm(forms.ModelForm):
	class Meta:
		model = MainExam
		fields = ('name', 'description')
		widgets = {
			'description': forms.Textarea(),
		}

class ExamCategoryForm(forms.ModelForm):
	subjects = forms.ModelMultipleChoiceField(
			queryset=Subject.objects.all(),
			widget=forms.CheckboxSelectMultiple(
				attrs={'class':'form-check-input'}),
			required=True)
	class Meta:
		model = ExamCategory
		fields = ('name', 'description', 'main_exam', 'subjects')
		widgets = {
			'description': forms.Textarea(),
		}