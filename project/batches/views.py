from django.shortcuts import render
from django.contrib.auth.models import User
from accounts.models import Role
from .models import Batch, BatchTiming
from test_app.models import Test
from .forms import BatchForm, BatchTimingForm
# CBS Views
from django.views.generic.list import ListView
from django.views.generic.edit import FormView, UpdateView
from django.views import View
# Mixins and decorators
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from accounts.mixins import AdminRedirectMixin, StudentRedirectMixin
# Response objects
import json, datetime
from django.template.loader import render_to_string
from django.http import JsonResponse

@login_required
def get_batch_form(request):
	form = BatchForm()
	return render(request, 'batches/create_batch.html', {'form': form})

@login_required
def get_batch_timing_form(request):
	form = BatchTimingForm()
	return render(request, 'batches/create_batch_timing.html', {'form': form})

# Create your views here.
class AdminBatchesView(LoginRequiredMixin, AdminRedirectMixin, ListView):
	template_name = "batches/admin_batches.html"
	model = Batch
	context_object_name = "batches"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context.update({'form': BatchForm()})
		return context

class CreateBatchView(LoginRequiredMixin, AdminRedirectMixin, FormView):
	form_class = BatchForm
	submit_response = "batches/create_batch_response.html"
	table = "batches/admin_batch_list.html"

	def form_valid(self, form):
		# Saving batch
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
		# Saving batch
		batch = form.save(commit=False)
		batch.modified_by = self.request.user
		batch.save()
		form.save_m2m()

		# Reponse
		table_response = render_to_string(self.table, {'batches': Batch.objects.all()})
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

	# def get_context_data(self, **kwargs):
	# 	context = super().get_context_data(**kwargs)
	# 	students = Role.objects.filter(name="student").values_list('users__username', 'users__id')
	# 	existing_students = self.object.students.values_list('username', flat=True)
	# 	context.update({'students': students, 'existing_students': existing_students})
	# 	return context

# Create your views here.
class BatchTimingsView(LoginRequiredMixin, AdminRedirectMixin, ListView):
	template_name = "batches/batch_timings.html"
	model = BatchTiming
	context_object_name = "batch_timings"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		batches = Batch.objects.all()
		context.update({'form': BatchTimingForm(), 'batches': batches})
		return context

class CreateBatchTimingView(LoginRequiredMixin, AdminRedirectMixin, FormView):
	form_class = BatchTimingForm
	submit_response = "batches/create_batch_timing_response.html"
	table = "batches/batch_timing_list.html"

	def form_valid(self, form):
		# Saving batch timing
		form.save()

		# Sending response
		response1 = render_to_string(self.submit_response, {'success': True})
		response2 = render_to_string(self.table, 
			{'batches': Batch.objects.all(), 'batch_timings': BatchTiming.objects.all()})
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
		response2 = render_to_string(self.table, 
			{'batches': Batch.objects.all(), 'batch_timings': BatchTiming.objects.all()})
		response = {
			'response1': response1, 'response2': response2
		}
		return JsonResponse(response)

class DeleteBatchTimingView(LoginRequiredMixin, AdminRedirectMixin, View):
	table = "batches/batch_timing_list.html"
	def post(self, request, batch_timing_id):
		# Deleting batch
		batch_timing = BatchTiming.objects.get(id=batch_timing_id)
		batch_timing.delete()

		# Reponse
		table_response = render_to_string(self.table, 
			{'batches': Batch.objects.all(), 'batch_timings': BatchTiming.objects.all()})
		return JsonResponse(table_response, safe=False)

class EditBatchTimingView(LoginRequiredMixin, AdminRedirectMixin, UpdateView):
	template_name = 'batches/edit_batch_timing.html'
	model = BatchTiming
	form_class = BatchTimingForm
	table = "batches/batch_timing_list.html"
	pk_url_kwarg = "batch_timing_id"

	def form_valid(self, form):
		# Saving batch timing
		form.save()

		# Reponse
		table_response = render_to_string(self.table, 
			{'batches': Batch.objects.all(), 'batch_timings': BatchTiming.objects.all()})
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

class StudentBatchView(LoginRequiredMixin, StudentRedirectMixin, UpdateView):
	template_name = "batches/student/batch.html"

	def get(self, request, batch_id):
		request.session['batch_id'] = batch_id
		now = datetime.datetime.now().time()
		today = datetime.date.today()
		test_list = []
		tests = Test.objects.filter(batch_id=batch_id, date_scheduled__gte=today)
		for test in tests:
			if test.date_scheduled == today:
				if test.closing_time > now:
					test_list.append(test)
			else:
				test_list.append(test)
		batch_timings = BatchTiming.objects.filter(batch_id=batch_id)
		context = {'tests': tests, 'batch_timings': batch_timings}
		return render(request, self.template_name, context)