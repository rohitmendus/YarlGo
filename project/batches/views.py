from django.shortcuts import render
from django.contrib.auth.models import User
from accounts.models import Role
from .models import Batch
from .forms import BatchForm
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
def get_batch_form(request):
	form = BatchForm()
	students = Role.objects.filter(name="student").values_list('users__username', 'users__id')
	return render(request, 'batches/create_batch.html', {'form': form, 'students': students})

# Create your views here.
class AdminBatchesView(LoginRequiredMixin, AdminRedirectMixin, ListView):
	template_name = "batches/admin_batches.html"
	model = Batch
	context_object_name = "batches"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		students = Role.objects.filter(name="student").values_list('users__username', 'users__id')
		context.update({'form': BatchForm(), 'students': students})
		return context

class CreateBatchView(LoginRequiredMixin, AdminRedirectMixin, FormView):
	form_class = BatchForm
	submit_response = "batches/create_batch_response.html"
	table = "batches/admin_batch_list.html"

	def form_valid(self, form):
		# Saving subject
		batch = form.save(commit=False)
		batch.created_by = self.request.user
		batch.modified_by = self.request.user
		batch.save()
		form.save_m2m()

		# Sending response
		response1 = render_to_string(self.submit_response, {'success': True})
		students = Role.objects.filter(name="student").values_list('users__username', 'users__id')
		response2 = render_to_string(self.table, {'batches': Batch.objects.all(), 'students': students})
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
		students = Role.objects.filter(name="student").values_list('users__username', 'users__id')
		response2 = render_to_string(self.table, {'batches': Batch.objects.all(), 'students': students})
		response = {
			'response1': response1, 'response2': response2
		}
		return JsonResponse(response)

class DeleteBatchView(LoginRequiredMixin, AdminRedirectMixin, View):
	table = "batches/admin_batch_list.html"
	def post(self, request, batch_id):
		# Deleting batch
		batch = Batch.objects.get(id=batch_id)
		batch.delete()

		# Reponse
		students = Role.objects.filter(name="student").values_list('users__username', 'users__id')
		table_response = render_to_string(self.table, {'batches': Batch.objects.all(), 'students': students})
		return JsonResponse(table_response, safe=False)

class EditBatchView(LoginRequiredMixin, AdminRedirectMixin, UpdateView):
	template_name = 'batches/edit_batch.html'
	model = Batch
	form_class = BatchForm
	table = "batches/admin_batch_list.html"
	pk_url_kwarg = "batch_id"

	def form_valid(self, form):
		# Saving subject
		batch = form.save(commit=False)
		batch.modified_by = self.request.user
		batch.save()
		form.save_m2m()

		# Reponse
		students = Role.objects.filter(name="student").values_list('users__username', 'users__id')
		table_response = render_to_string(self.table, {'batches': Batch.objects.all(), 'students': students})
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

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		students = Role.objects.filter(name="student").values_list('users__username', 'users__id')
		existing_students = self.object.students.values_list('username', flat=True)
		context.update({'students': students, 'existing_students': existing_students})
		return context