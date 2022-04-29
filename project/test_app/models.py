from django.db import models
from django.contrib.auth.models import User
from subjects.models import Topic

# Create your models here.
class Option(models.Model):
	text = models.CharField(max_length=200)

	def __str__(self):
		return self.text

class Question(models.Model):
	question = models.CharField(max_length=500, unique=True)
	topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name="questions")
	answer = models.ForeignKey(Option, related_name="question")
	options = models.ManyToManyField(Option, related_name="question")
	created_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name="questions_created")
	modified_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name="questions_modified")
	date_created = models.DateTimeField(auto_now_add=True)
	date_modified = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.question

class Test(models.Model):
	name = models.CharField(max_length=200, unique=True)
	no_of_questions = models.PositiveIntegerField()
	cutoff_mark = models.FloatField()
	max_mark = models.FloatField()
	date_scheduled = models.DateField()
	opening_time = models.TimeField()
	closing_time = models.TimeField()
	topics =  models.ManyToManyField(Topic, related_name="tests")
	created_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name="tests_created")
	modified_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name="tests_modified")
	date_created = models.DateTimeField(auto_now_add=True)
	date_modified = models.DateTimeField(auto_now=True)

class TopicDistribution(models.Model):
	topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
	test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name="topic_distribution")
	no_of_questions = models.PositiveIntegerField()
	max_mark = models.FloatField()

class UserQuestion(models.Model):
	STATE_CHOICES = [
        (0, 'Wrong'),
        (1, 'Correct'),
        (2, 'Unanswered')
    ]

	question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="user_reports")
	option_choosen = models.ForeignKey(Option, related_name="user_reports", null=True, blank=True)
	time_taken = models.DurationField()
	state = models.IntegerField(default=2, choices=STATE_CHOICES)
	test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name="questions")
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="test_questions")

class UserTest(models.Model):
	test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name="reports")
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="test_reports")
	# state = models.IntegerField(default=0, choices=STATE_CHOICES)
	# passed = models.BooleanField()
	marks_gained = models.FloatField(null=True, blank=True)
	time_taken = models.DurationField(null=True, blank=True)

	@property
	def percentage(self):
		return (float(self.marks_gained) / float(self.test.max_mark)) * 100

	@property
	def passed(self):
		if self.marks_gained >= self.test.cutoff_mark:
			return True
		else:
			return False

	# @property
	# def time_per_question(self):
	# 	pass

class TopicPerformance(models.Model):
	test_topic = models.ForeignKey(TopicDistribution, on_delete=models.CASCADE, related_name="topic_performance")
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="test_topic_reports")
	marks_gained = models.FloatField(null=True, blank=True)
	time_taken = models.DurationField(null=True, blank=True)

	@property
	def percentage(self):
		return (float(self.marks_gained) / float(self.test_topic.max_mark)) * 100
