from django.db import models
from django.contrib.auth.models import User
from subjects.models import Subject

# Create your models here.
class MainExam(models.Model):
	name = models.CharField(max_length=200, unique=True)
	description = models.CharField(max_length=500, blank=True)
	created_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name="exams_created")
	modified_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name="exams_modified")
	date_created = models.DateTimeField(auto_now_add=True)
	date_modified = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.name

class ExamCategory(models.Model):
	name = models.CharField(max_length=200, unique=True)
	description = models.CharField(max_length=500, blank=True)
	created_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name="exams_categories_created")
	modified_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name="exams_categories_modified")
	date_created = models.DateTimeField(auto_now_add=True)
	date_modified = models.DateTimeField(auto_now=True)
	main_exam = models.ForeignKey(MainExam, on_delete=models.CASCADE, related_name="exams_categories")
	subjects = models.ManyToManyField(Subject, related_name="exam_categories", blank=True)

	@property
	def subject_list(self):
		subject_s = list(self.subjects.values_list('name', flat=True))
		return ', '.join(subject_s)
	

	def __str__(self):
		return self.name