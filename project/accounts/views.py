from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CustomUserCreationForm
from .models import Profile
from django.views.generic import TemplateView
from django.views.generic.edit import FormView

# Create your views here.
class DashboardView(LoginRequiredMixin, TemplateView):
	template_name = "accounts/dashboard.html"

class UserFormView(FormView):
	template_name = "accounts/users.html"
	form_class = CustomUserCreationForm

	def form_valid(self, form):
		user = form.save()
		profile = Profile.objects.create(user=user)
		form.send_email()
		return render(request, 'user_created.html')
