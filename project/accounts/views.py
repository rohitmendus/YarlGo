# Response functions
from django.template.loader import render_to_string
from django.http import HttpResponse, JsonResponse
import json
from django.shortcuts import render, redirect
# Mixins
from django.contrib.auth.mixins import LoginRequiredMixin
# Forms
from .forms import CustomUserCreationForm
# Models
from .models import Profile, Role
from django.contrib.auth.models import User
# CBS Views
from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView
from django.views import View
# Others
from django.conf import settings
from django.core.mail import send_mail


def redirect_dashboard(request):
	return redirect('/dashboard')

def get_user_form(request):
	form = CustomUserCreationForm()
	context = {'form': form, 'password': User.objects.make_random_password()}
	context['roles'] = Role.objects.values_list('name', flat=True)
	return render(request, 'accounts/create_user_form.html', context)

def check_username(request):
	username = request.GET.get('username')
	if User.objects.filter(username=username).exists():
		return HttpResponse("<span style='color:red;'>This username already exixts!</span>")
	else:
		return HttpResponse("<span style='color:green;'>This username is available</span>")

class CreateUserView(View):
	submit_response = 'accounts/create_user_response.html'
	table = 'accounts/user_list.html'
	def post(self, request):
		form = CustomUserCreationForm(request.POST)
		if form.is_valid():
			password = request.POST.get('password1')
			user_roles = request.POST.getlist('user_role')
			# Saving user
			user = form.save()
			profile = Profile.objects.create(user=user)

			# Adding user roles
			for i in user_roles:
				role = Role.objects.get(name=i)
				role.users.add(user)

			response_context = {'success': True}

			# Sending welcome mail
			subject = f'Welcome {user.first_name} to YarlGo!'
			email_context = {'name':user.first_name, 'username':user.username, 
				'password': password}
			body = render_to_string('emails/welcome_user_mail.html', email_context)
			send_mail(
			    subject,
			    body,
			    settings.EMAIL_HOST_USER,
			    [user.email],
			    fail_silently=False,
			)
		else:
			error_messages = []
			errors = json.loads(form.errors.as_json())
			for x in errors:
				for y in errors[x]:
					error_messages.append(y['message'])
			response_context = {'success': False, 'errors': error_messages}
		response1 = render_to_string(self.submit_response, response_context)
		response2 = render_to_string(self.table, {'users': Profile.objects.all(),
			'roles': Role.objects.values_list('name', flat=True)})
		response = {
			'response1': response1, 'response2': response2
		}
		return JsonResponse(response)

class DeleteUserView(View):
	table = 'accounts/user_list.html'
	def post(self, request, id):
		# Deleting user
		user = User.objects.get(id=id)
		user.delete()

		# Reponse
		table_response = render_to_string(self.table, {'users': Profile.objects.all(),
			'roles': Role.objects.values_list('name', flat=True)})
		return JsonResponse(table_response, safe=False)

class EditUserView(UpdateView):
	template_name = 'accounts/edit_user_form.html'
	model = User
	fields = ['first_name','last_name', 'username', 'email']
	roles = Role.objects.values_list('name', flat=True)
	table = 'accounts/user_list.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['roles'] = self.roles
		context['user_role'] = Profile.objects.get(user_id=self.kwargs.get('pk')).role
		return context

	def form_valid(self, form):
		user_roles = self.request.POST.getlist('user_edit_role')
		user = form.save()
		for role in user.roles.all():
			if role.name not in user_roles:
				role.users.remove(user)
		for role_name in user_roles:
			role = Role.objects.get(name=role_name)
			role.users.add(user)

		# Reponse
		table_response = render_to_string(self.table, {'users': Profile.objects.all(),
			'roles': Role.objects.values_list('name', flat=True)})

		response = {'success': True, 'table_response': table_response}
		return JsonResponse(response)

	def form_invalid(self, form):
		error_messages = []
		errors = json.loads(form.errors.as_json())
		for x in errors:
			for y in errors[x]:
				error_messages.append(y['message'])
		
		# Reponse
		table_response = render_to_string(self.table, {'users': Profile.objects.all(),
			'roles': Role.objects.values_list('name', flat=True)})
		response = {'success': False, 'errors': error_messages}
		return JsonResponse(response)


# Create your views here.
class DashboardView(LoginRequiredMixin, TemplateView):
	template_name = "accounts/dashboard.html"


class UsersView(ListView):
	template_name = "accounts/users.html"
	model = Profile
	context_object_name = "users"
	roles = Role.objects.values_list('name', flat=True)
	form = CustomUserCreationForm()

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context.update({'password': User.objects.make_random_password(),
			'roles': self.roles, 'form': self.form})
		return context
		
