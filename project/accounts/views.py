from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from .forms import CustomUserCreationForm
from .models import Profile, Role
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.http import HttpResponse

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

# Create your views here.
class DashboardView(LoginRequiredMixin, TemplateView):
	template_name = "accounts/dashboard.html"

class UserFormView(FormView):
	template_name = "accounts/users.html"
	form_class = CustomUserCreationForm
	roles = Role.objects.values_list('name', flat=True)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['password'] = User.objects.make_random_password()
		context['roles'] = self.roles
		return context

	def form_valid(self, form):
		password = self.request.POST.get('password1')
		user_roles = self.request.POST.getlist('user_role')
		# Saving user
		user = form.save()
		profile = Profile.objects.create(user=user)

		# Adding user roles
		for i in user_roles:
			role = Role.objects.get(name=i)
			role.users.add(user)

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
		return render(self.request, 'accounts/user_created.html')
