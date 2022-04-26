from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.edit import FormView, UpdateView
from django.views import View
from .models import MainExam, ExamCategory
from .forms import MainExamForm, ExamCategoryForm
import json
from django.template.loader import render_to_string
from django.http import JsonResponse
# Mixins and decorators
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from accounts.mixins import AdminRedirectMixin

@login_required
def get_exam_form(request):
	form = MainExamForm()
	return render(request, 'exams/create_exam.html', {'form': form})

@login_required
def get_exam_cat_form(request):
	form = ExamCategoryForm()
	return render(request, 'exams/create_exam_category.html', {'form': form})

# Create your views here.
class MainExamsView(LoginRequiredMixin, AdminRedirectMixin, ListView):
	template_name = "exams/exams.html"
	model = MainExam
	context_object_name = "exams"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context.update({'form': MainExamForm()})
		return context

class CreateMainExamView(LoginRequiredMixin, AdminRedirectMixin, FormView):
	form_class = MainExamForm
	submit_response = "exams/create_exam_response.html"
	table = "exams/exam_list.html"

	def form_valid(self, form):
		exam = form.save(commit=False)
		exam.created_by = self.request.user
		exam.modified_by = self.request.user
		exam.save()

		# Sending response
		response1 = render_to_string(self.submit_response, {'success': True})
		response2 = render_to_string(self.table, {'exams': MainExam.objects.all()})
		response = {
			'response1': response1, 'response2': response2
		}
		return JsonResponse(response)

	def form_invalid(self, form):
		# Collecting error messages
		error_messages = []
		errors = json.loads(form.errors.as_json())
		for x in errors:
			for y in errors[x]:
				error_messages.append(y['message'])
		
		# Sending response
		response1 = render_to_string(self.submit_response, {'success': False, 
			'errors': error_messages})
		response2 = render_to_string(self.table, {'exams': MainExam.objects.all()})
		response = {
			'response1': response1, 'response2': response2
		}
		return JsonResponse(response)

class DeleteMainExamView(LoginRequiredMixin, AdminRedirectMixin, View):
	table = 'exams/exam_list.html'
	def post(self, request, exam_id):
		# Deleting exam
		exam = MainExam.objects.get(id=exam_id)
		exam.delete()

		# Reponse
		table_response = render_to_string(self.table, {'exams': MainExam.objects.all()})
		return JsonResponse(table_response, safe=False)

class EditMainExamView(LoginRequiredMixin, AdminRedirectMixin, UpdateView):
	template_name = 'exams/edit_exam.html'
	model = MainExam
	form_class = MainExamForm
	table = 'exams/exam_list.html'
	pk_url_kwarg = "exam_id"

	def form_valid(self, form):
		exam = form.save(commit=False)
		exam.modified_by = self.request.user
		exam.save()

		# Reponse
		table_response = render_to_string(self.table, {'exams': MainExam.objects.all()})

		response = {'success': True, 'table_response': table_response}
		return JsonResponse(response)

	def form_invalid(self, form):
		error_messages = []
		errors = json.loads(form.errors.as_json())
		for x in errors:
			for y in errors[x]:
				error_messages.append(y['message'])
		
		# Reponse
		response = {'success': False, 'errors': error_messages}
		return JsonResponse(response)

class ExamCategoriesView(LoginRequiredMixin, AdminRedirectMixin, ListView):
	template_name = "exams/exam_categories.html"
	model = ExamCategory
	context_object_name = "exam_cats"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context.update({'form': ExamCategoryForm()})
		return context

class CreateExamCategory(LoginRequiredMixin, AdminRedirectMixin, FormView):
	form_class = ExamCategoryForm
	submit_response = "exams/create_exam_category_response.html"
	table = "exams/exam_category_list.html"

	def form_valid(self, form):
		exam_cat = form.save(commit=False)
		exam_cat.created_by = self.request.user
		exam_cat.modified_by = self.request.user
		exam_cat.save()

		# Sending response
		response1 = render_to_string(self.submit_response, {'success': True})
		response2 = render_to_string(self.table, {'exam_cats': ExamCategory.objects.all()})
		response = {
			'response1': response1, 'response2': response2
		}
		return JsonResponse(response)

	def form_invalid(self, form):
		# Collecting error messages
		error_messages = []
		errors = json.loads(form.errors.as_json())
		for x in errors:
			for y in errors[x]:
				error_messages.append(y['message'])
		
		# Sending response
		response1 = render_to_string(self.submit_response, {'success': False, 
			'errors': error_messages})
		response2 = render_to_string(self.table, {'exam_cats': ExamCategory.objects.all()})
		response = {
			'response1': response1, 'response2': response2
		}
		return JsonResponse(response)

class DeleteExamCategoryView(LoginRequiredMixin, AdminRedirectMixin, View):
	table = 'exams/exam_category_list.html'
	def post(self, request, exam_cat_id):
		# Deleting exam
		exam_cat = ExamCategory.objects.get(id=exam_cat_id)
		exam_cat.delete()

		# Reponse
		table_response = render_to_string(self.table, {'exam_cats': ExamCategory.objects.all()})
		return JsonResponse(table_response, safe=False)

class EditExamCategoryView(LoginRequiredMixin, AdminRedirectMixin, UpdateView):
	template_name = 'exams/edit_exam_category.html'
	model = ExamCategory
	form_class = ExamCategoryForm
	table = 'exams/exam_category_list.html'
	pk_url_kwarg = "exam_cat_id"

	def form_valid(self, form):
		exam_cat = form.save(commit=False)
		exam_cat.modified_by = self.request.user
		exam_cat.save()

		# Reponse
		table_response = render_to_string(self.table, {'exam_cats': ExamCategory.objects.all()})

		response = {'success': True, 'table_response': table_response}
		return JsonResponse(response)

	def form_invalid(self, form):
		error_messages = []
		errors = json.loads(form.errors.as_json())
		for x in errors:
			for y in errors[x]:
				error_messages.append(y['message'])
		
		# Reponse
		response = {'success': False, 'errors': error_messages}
		return JsonResponse(response)