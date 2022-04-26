from django.shortcuts import render
from .models import Subject, FacultyRight, Right
from accounts.models import Role
from django.contrib.auth.models import User
from .forms import SubjectForm
# CBS Views
from django.views.generic.list import ListView
from django.views.generic.edit import FormView, UpdateView
from django.views import View
# Mixins and decorators
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from accounts.mixins import AdminRedirectMixin
# Response objects
import json
from django.template.loader import render_to_string
from django.http import JsonResponse

@login_required
def get_subject_form(request):
	form = SubjectForm()
	return render(request, 'subjects/create_subject.html', {'form': SubjectForm()})

# Create your views here.
class AdminSubjectsView(LoginRequiredMixin, AdminRedirectMixin, ListView):
	template_name = "subjects/admin_subjects.html"
	model = Subject
	context_object_name = "subjects"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		faculties = Role.objects.filter(name="faculty").values_list('users__username', flat=True)
		context.update({'form': SubjectForm(), 'faculties': faculties})
		return context

class CreateSubjectView(LoginRequiredMixin, AdminRedirectMixin, FormView):
	form_class = SubjectForm
	submit_response = "subjects/create_subject_response.html"
	table = "subjects/subject_list.html"

	def form_valid(self, form):
		examiners = self.request.POST.getlist('examiners')
		staff = self.request.POST.getlist('staff')
		# Saving subject
		subject = form.save(commit=False)
		subject.created_by = self.request.user
		subject.modified_by = self.request.user
		subject.save()

		# Adding examiners
		examiner_right = Right.objects.get(name="examiner")
		for i in examiners:
			user = 	User.objects.get(username=i)
			FacultyRight.objects.create(user=user, subject=subject, right=examiner_right)

		# Adding staff
		staff_right = Right.objects.get(name="staff")
		for i in staff:
			user = 	User.objects.get(username=i)
			FacultyRight.objects.create(user=user, subject=subject, right=staff_right)

		# Sending response
		response1 = render_to_string(self.submit_response, {'success': True})
		faculties = Role.objects.filter(name="faculty").values_list('users__username', flat=True)
		response2 = render_to_string(self.table, {'subjects': Subject.objects.all(), 
			'faculties': faculties})
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
		faculties = Role.objects.filter(name="faculty").values_list('users__username', flat=True)
		response2 = render_to_string(self.table, {'subjects': Subject.objects.all(), 
			'faculties': faculties})
		response = {
			'response1': response1, 'response2': response2
		}
		return JsonResponse(response)

class DeleteSubjectView(LoginRequiredMixin, AdminRedirectMixin, View):
	table = 'exams/exam_list.html'
	def post(self, request, subject_id):
		# Deleting exam
		exam = Subject.objects.get(id=exam_id)
		exam.delete()

		# Reponse
		faculties = Role.objects.filter(name="faculty").values_list('users__username', flat=True)
		table_response = render_to_string(self.table, {'subjects': Subject.objects.all(), 
			'faculties': faculties})
		return JsonResponse(table_response, safe=False)

class EditSubjectView(LoginRequiredMixin, AdminRedirectMixin, UpdateView):
	template_name = 'exams/edit_exam.html'
	model = Subject
	form_class = SubjectForm
	table = 'subjects/exam_list.html'
	pk_url_kwarg = "subject_id"

	def form_valid(self, form):
		exam = form.save(commit=False)
		exam.modified_by = self.request.user
		exam.save()

		# Reponse
		faculties = Role.objects.filter(name="faculty").values_list('users__username', flat=True)
		table_response = render_to_string(self.table, {'subjects': Subject.objects.all(), 
			'faculties': faculties})
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