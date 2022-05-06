from django.db import models
from django.contrib.auth.models import User
from exams.models import ExamCategory
from subjects.models import Subject

# Create your models here.
class Batch(models.Model):
	name = models.CharField(max_length=200, unique=True)
	opening_date = models.DateField()
	closing_date = models.DateField()
	exam_category = models.ForeignKey(ExamCategory, on_delete=models.CASCADE, related_name="batches")
	created_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name="batches_created")
	modified_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name="batches_modified")
	date_created = models.DateTimeField(auto_now_add=True)
	date_modified = models.DateTimeField(auto_now=True)
	students = models.ManyToManyField(User, related_name="batches")

	@property
	def student_list(self):
		student_s = []
		for student in self.students.values_list('first_name', 'last_name'):
			name = f'{student[0]} {student[1]}'
			student_s.append(name)
		return ', '.join(student_s)

	# @property
	# def subjects(self):
	# 	return self.exam_category.subjects

	def __str__(self):
		return self.name +" - "+ self.exam_category.name

class BatchTiming(models.Model):
	class Meta:
		ordering = ['opening_time']

	opening_time = models.TimeField()
	closing_time = models.TimeField()
	batch = models.ForeignKey(Batch, on_delete=models.CASCADE, related_name="batch_timings")
	subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="subject_timings")