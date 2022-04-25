from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

# Create your models here.
class Profile(models.Model):
	phoneNumberRegex = RegexValidator(regex = r"^\+?1?\d{8,15}$",
		message='Phone Number is invalid!',
		code='invalid')
	sex_type = (
		("Male", "Male"),
		("Female", "Female"),
		("Unspecified", "Unspecified"),
	)
	salutations = (
		("Dr", "Dr"),
		("Mr", "Mr"),
		("Ms", "Ms"),
		("Prof", "Prof"),
		("Rev", "Rev"),
	)
	phone = models.CharField(validators = [phoneNumberRegex], max_length=10, 
		unique = True, blank=True, null=True,
		error_messages={'unique': 'The phone number you entered has already been registered!'})
	age = models.PositiveIntegerField(blank=True, null=True)
	sex = models.CharField(choices=sex_type, max_length=15, blank=True)
	salutation = models.CharField(choices=salutations, max_length=15, default="Mr")
	avatar = models.ImageField(upload_to="pics", blank=True)
	user = models.OneToOneField(User, on_delete=models.CASCADE)

	def __str__(self):
		return self.user.first_name

	def is_avatar_empty(self):
		if (not self.avatar):
			return True
		return False

	@property
	def full_name(self):
		return f'{self.user.first_name} {self.user.last_name}'

	@property
	def role(self):
		try:
			return str(self.user.roles.all()[0]).strip()
		except:
			return ""

class Role(models.Model):
	name = models.CharField(max_length=100, blank=False, null=False)
	description = models.CharField(max_length=500, blank=True, null=False)
	users = models.ManyToManyField(User, related_name="roles", blank=True)

	def __str__(self):
		return self.name