from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Subject(models.Model):
	name = models.CharField(max_length=200, unique=True)
	description = models.CharField(max_length=500, blank=True)
	created_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name="subjects_created")
	modified_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name="subjects_modified")
	date_created = models.DateTimeField(auto_now_add=True)
	date_modified = models.DateTimeField(auto_now=True)

	@property
	def examiners(self):
		examiner_users = list(self.faculty_rights.filter(right__name="examiner").values_list('user__username', flat=True))
		return ', '.join(examiner_users)

	@property
	def staff(self):
		staff_users = list(self.faculty_rights.filter(right__name="staff").values_list('user__username', flat=True))
		return ', '.join(staff_users)

class Topic(models.Model):
	name = models.CharField(max_length=200, unique=True)
	description = models.CharField(max_length=500, blank=True)
	created_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name="topics_created")
	modified_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name="topics_modified")
	date_created = models.DateTimeField(auto_now_add=True)
	date_modified = models.DateTimeField(auto_now=True)
	subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="topics")

class Right(models.Model):
	name = models.CharField(max_length=200, unique=True)
	description = models.CharField(max_length=500, blank=True)

class FacultyRight(models.Model):
	right = models.ForeignKey(Right, on_delete=models.CASCADE)
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="subject_rights")
	subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="faculty_rights")
