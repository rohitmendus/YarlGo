# Models
from django.contrib.auth.models import User
from subjects.models import Topic, Subject
from batches.models import Batch
from .models import Option, Question, Test
from .forms import TopicDistributionForm, TestForm
from django.forms import formset_factory
# CBS Views
from django.views import View
# Mixins and decorators
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from accounts.mixins import FacultyRedirectMixin
# Response objects
import json
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.shortcuts import render
from django.shortcuts import redirect
from django.core.exceptions import ValidationError
import datetime

def get_time_difference(a, b):
	dateTimeA = datetime.datetime.combine(datetime.date.today(), a)
	dateTimeB = datetime.datetime.combine(datetime.date.today(), b)
	dateTimeDifference = dateTimeA - dateTimeB  
	return dateTimeDifference.total_seconds()

@login_required
def get_back_test(request):
	subject = Subject.objects.get(id=request.session['subject_id'])

	context = {}
	batches = Batch.objects.filter(exam_category__subjects=subject)
	context['batches'] = batches
	context['test_form'] = TestForm
	TopicDistributionFormSet = formset_factory(TopicDistributionForm)
	context['test_topic_form'] = TopicDistributionFormSet(form_kwargs={'request': request})
	tests = []
	test_objs = Test.objects.all()
	topic_ids = list(Topic.objects.filter(subject=subject).values_list('id', flat=True))
	for test_obj in test_objs:
		for topic_dist in test_obj.distributions['topics']:
			if topic_dist['topic_id'] in topic_ids:
				tests.append(test_obj)
				break
	context['tests'] = tests

	return render(request, 'tests/faculty/tests.html', context)

class CreateQuestionView(LoginRequiredMixin, FacultyRedirectMixin, View):
	submit_response = "tests/faculty/create_question_response.html"
	table = "tests/faculty/question_list.html"

	def post(self, request):
		subject = Subject.objects.get(id=request.session['subject_id'])
		question = request.POST.get('question')
		topic_name = request.POST.get('topic')
		topic = Topic.objects.get(name=topic_name)
		answer_opt = request.POST.get('answer')
		
		question_obj = Question(question=question, topic=topic, 
			created_by=request.user, modified_by=request.user)
		option1 = Option(text=request.POST.get('option1'))
		option2 = Option(text=request.POST.get('option2'))
		option3 = Option(text=request.POST.get('option3'))
		option4 = Option(text=request.POST.get('option4'))

		try:
			question_obj.full_clean(exclude=["answer"])
			option1.full_clean()
			option2.full_clean()
			option3.full_clean()
			option4.full_clean()
		except ValidationError as e:
			error_messages = []
			errors = e.message_dict
			for x in errors:
				for y in errors[x]:
					error_messages.append(y)
			# Sending response
			response1 = render_to_string(self.submit_response, {'success': False, 
				'errors': error_messages})
			response2 = render_to_string(self.table, {'questions': Question.objects.filter(topic__subject=subject),
				'topics': Topic.objects.filter(subject=subject)})
			response = {
				'response1': response1, 'response2': response2
			}
			return JsonResponse(response)
		else:
			option1.save()
			option2.save()
			option3.save()
			option4.save()

			if answer_opt == "1":
				question_obj.answer = option1
			elif answer_opt == "2":
				question_obj.answer = option2
			elif answer_opt == "3":
				question_obj.answer = option3
			elif answer_opt == "4":
				question_obj.answer = option4

			question_obj.save()
			question_obj.options.add(option1, option2, option3, option4)
			
			# Sending response
			response1 = render_to_string(self.submit_response, {'success': True})
			response2 = render_to_string(self.table, {'questions': Question.objects.filter(topic__subject=subject),
				'topics': Topic.objects.filter(subject=subject)})
			response = {
				'response1': response1, 'response2': response2
			}
			return JsonResponse(response)

	def get(self, request):
		subject = Subject.objects.get(id=request.session['subject_id'])
		context = {'topics': Topic.objects.filter(subject=subject)}
		return render(request, 'tests/faculty/create_question.html', context)

class DeleteQuestionView(LoginRequiredMixin, FacultyRedirectMixin, View):
	table = 'tests/faculty/question_list.html'
	def post(self, request, question_id):
		subject = Subject.objects.get(id=self.request.session['subject_id'])
		# Deleting question
		question = Question.objects.get(id=question_id)
		question.delete()

		# Reponse
		table_response = render_to_string(self.table, {'questions': Question.objects.filter(topic__subject=subject),
			'topics': Topic.objects.filter(subject=subject)})
		return JsonResponse(table_response, safe=False)

class EditQuestionView(LoginRequiredMixin, FacultyRedirectMixin, View):
	template_name = 'tests/faculty/edit_question.html'
	table = 'tests/faculty/question_list.html'

	def get(self, request, question_id):
		subject = Subject.objects.get(id=self.request.session['subject_id'])
		question = Question.objects.get(id=question_id)
		topics = Topic.objects.filter(subject=subject)
		return render(request, self.template_name, {"question": question, 
			"topics": topics})

	def post(self, request, question_id):
		subject = Subject.objects.get(id=request.session['subject_id'])
		question = request.POST.get('edit_question')
		topic_name = request.POST.get('edit_topic')
		topic = Topic.objects.get(name=topic_name)
		answer_opt = request.POST.get('edit_answer')
		
		question_obj = Question.objects.get(id=question_id)
		question_obj.topic = topic
		question_obj.question = question
		question_obj.modified_by = request.user

		options = list(question_obj.options.all())
		option1 = options[0]
		option2 = options[1]
		option3 = options[2]
		option4 = options[3]

		option1.text = request.POST.get('edit_option1')
		option2.text = request.POST.get('edit_option2')
		option3.text = request.POST.get('edit_option3')
		option4.text = request.POST.get('edit_option4')

		try:
			question_obj.full_clean()
			option1.full_clean()
			option2.full_clean()
			option3.full_clean()
			option4.full_clean()
		except ValidationError as e:
			error_messages = []
			errors = e.message_dict
			for x in errors:
				for y in errors[x]:
					error_messages.append(y)

			# Reponse
			response = {'success': False, 'errors': error_messages}
			return JsonResponse(response)
		else:
			option1.save()
			option2.save()
			option3.save()
			option4.save()

			if answer_opt == "1":
				question_obj.answer = option1
			elif answer_opt == "2":
				question_obj.answer = option2
			elif answer_opt == "3":
				question_obj.answer = option3
			elif answer_opt == "4":
				question_obj.answer = option4

			question_obj.save()
			question_obj.options.add(option1, option2, option3, option4)

			# Reponse
			table_response = render_to_string(self.table, {'questions': Question.objects.filter(topic__subject=subject),
				'topics': Topic.objects.filter(subject=subject)})
			response = {'success': True, 'table_response': table_response}
			return JsonResponse(response)


class CreateTestView(LoginRequiredMixin, FacultyRedirectMixin, View):
	template = "tests/faculty/create_test.html"
	submit_response = "tests/faculty/create_test_response.html"
	table = "tests/faculty/test_list.html"

	def post(self, request):
		subject = Subject.objects.get(id=request.session['subject_id'])
		TestDistFormSet = formset_factory(TopicDistributionForm)
		test_dist = TestDistFormSet(request.POST, form_kwargs={'request': request})
		if test_dist.is_valid():
			post_data = request.POST.copy()
			total_no_of_questions = 0
			topics = []
			for form in test_dist:
				if 'topic' and 'no_of_questions' in form.cleaned_data:
					topic_obj = {}
					topic_id = form.cleaned_data['topic'].id
					no_of_questions = int(form.cleaned_data['no_of_questions'])
					total_no_of_questions += no_of_questions
					topic_obj["topic_id"] = topic_id
					topic_obj["no_of_questions"] = no_of_questions
					topic_obj["max_mark"] = no_of_questions
					topics.append(topic_obj)
			post_data.update({'no_of_questions': str(total_no_of_questions), 
				'max_mark': str(total_no_of_questions)})
			test_form = TestForm(post_data)
			if test_form.is_valid():
				print(test_form.cleaned_data)
				opening_time = test_form.cleaned_data['opening_time']
				closing_time = test_form.cleaned_data['closing_time']
				time = get_time_difference(closing_time, opening_time)
				distributions = {
					"cutoff_mark": test_form.cleaned_data['cutoff_mark'],
					"max_mark": test_form.cleaned_data['max_mark'],
					"no_of_questions": test_form.cleaned_data['no_of_questions'],
					"time": time,
					"topics": topics,
				}
				test = test_form.save(commit=False)
				test.created_by = request.user
				test.modified_by = request.user
				test.distributions = distributions
				print(distributions)
				test.save()

				# Sending response
				batches = Batch.objects.filter(exam_category__subjects=subject)
				tests = []
				test_objs = Test.objects.all()
				topic_ids = list(Topic.objects.filter(subject=subject).values_list('id', flat=True))
				for test_obj in test_objs:
					for topic_dist in test_obj.distributions['topics']:
						if topic_dist['topic_id'] in topic_ids:
							tests.append(test_obj)
							break

				context = {'batches': batches, 'tests': tests}

				response1 = render_to_string(self.submit_response, {'success': True})
				response2 = render_to_string(self.table, context)
				response = {
					'response1': response1, 'response2': response2
				}
				return JsonResponse(response)
			else:
				# Collecting error messages
				error_messages = []
				errors = json.loads(test_form.errors.as_json())
				for x in errors:
					for y in errors[x]:
						error_messages.append(y['message'])
				
				# Sending response
				batches = Batch.objects.filter(exam_category__subjects=subject)
				tests = []
				test_objs = Test.objects.all()
				topic_ids = list(Topic.objects.filter(subject=subject).values_list('id', flat=True))
				for test_obj in test_objs:
					for topic_dist in test_obj.distributions['topics']:
						if topic_dist['topic_id'] in topic_ids:
							tests.append(test_obj)
							break

				context = {'batches': batches, 'tests': tests}

				response1 = render_to_string(self.submit_response, {'success': False, 
					'errors': error_messages})
				response2 = render_to_string(self.table, context)
				response = {
					'response1': response1, 'response2': response2
				}
				return JsonResponse(response)
		else:
			# Collecting error messages
			error_messages = []
			errors = json.loads(test_dist.errors.as_json())
			for x in errors:
				for y in errors[x]:
					error_messages.append(y['message'])
			
			# Sending response
			batches = Batch.objects.filter(exam_category__subjects=subject)
			tests = []
			test_objs = Test.objects.all()
			topic_ids = list(Topic.objects.filter(subject=subject).values_list('id', flat=True))
			for test_obj in test_objs:
				for topic_dist in test_obj.distributions['topics']:
					if topic_dist['topic_id'] in topic_ids:
						tests.append(test_obj)
						break

			context = {'batches': batches, 'tests': tests}

			response1 = render_to_string(self.submit_response, {'success': False, 
				'errors': error_messages})
			response2 = render_to_string(self.table, context)
			response = {
				'response1': response1, 'response2': response2
			}
			return JsonResponse(response)

	def get(self, request):
		context = {}
		context['test_form'] = TestForm
		TopicDistributionFormSet = formset_factory(TopicDistributionForm)
		context['test_topic_form'] = TopicDistributionFormSet(form_kwargs={'request': request})

		return render(request, self.template, context)


class DeleteTestView(LoginRequiredMixin, FacultyRedirectMixin, View):
	table = 'tests/faculty/test_list.html'
	def post(self, request, test_id):
		subject = Subject.objects.get(id=self.request.session['subject_id'])
		# Deleting test
		test = Test.objects.get(id=test_id)
		test.delete()

		# Reponse
		batches = Batch.objects.filter(exam_category__subjects=subject)
		tests = []
		test_objs = Test.objects.all()
		topic_ids = list(Topic.objects.filter(subject=subject).values_list('id', flat=True))
		for test_obj in test_objs:
			for topic_dist in test_obj.distributions['topics']:
				if topic_dist['topic_id'] in topic_ids:
					tests.append(test_obj)
					break

			context = {'batches': batches, 'tests': tests}
		table_response = render_to_string(self.table, context)
		return JsonResponse(table_response, safe=False)


class DuplicateTestView(LoginRequiredMixin, FacultyRedirectMixin, View):
	template_name = "tests/faculty/duplicate_test.html"
	def get(self, request, test_id):
		test = Test.objects.get(id=test_id)
		topic_dist = test.distributions['topics']
		context = {}
		context['test_form'] = TestForm(instance=test)
		TopicDistributionFormSet = formset_factory(TopicDistributionForm, extra=len(topic_dist))
		context['test_topic_form'] = TopicDistributionFormSet(form_kwargs={'request': request})
		context['topic_dist'] = json.dumps(topic_dist)
		return render(request, self.template_name, context)

class EditTestView(LoginRequiredMixin, FacultyRedirectMixin, View):
	template_name = "tests/faculty/edit_test.html"
	def get(self, request, test_id):
		test = Test.objects.get(id=test_id)
		topic_dist = test.distributions['topics']
		context = {}
		context['test_form'] = TestForm(instance=test)
		TopicDistributionFormSet = formset_factory(TopicDistributionForm, extra=len(topic_dist))
		context['test_topic_form'] = TopicDistributionFormSet(form_kwargs={'request': request})
		context['topic_dist'] = json.dumps(topic_dist)
		return render(request, self.template_name, context)

	def post(self, request, test_id):
		response = {}
		subject = Subject.objects.get(id=request.session['subject_id'])
		instance = Test.objects.get(id=test_id)
		TestDistFormSet = formset_factory(TopicDistributionForm)
		test_dist = TestDistFormSet(request.POST, form_kwargs={'request': request})
		if test_dist.is_valid():
			post_data = request.POST.copy()
			total_no_of_questions = 0
			topics = []
			for form in test_dist:
				if 'topic' and 'no_of_questions' in form.cleaned_data:
					topic_obj = {}
					topic_id = form.cleaned_data['topic'].id
					no_of_questions = int(form.cleaned_data['no_of_questions'])
					total_no_of_questions += no_of_questions
					topic_obj["topic_id"] = topic_id
					topic_obj["no_of_questions"] = no_of_questions
					topic_obj["max_mark"] = no_of_questions
					topics.append(topic_obj)
			post_data.update({'no_of_questions': str(total_no_of_questions), 
				'max_mark': str(total_no_of_questions)})
			test_form = TestForm(post_data, instance=instance)
			if test_form.is_valid():
				opening_time = test_form.cleaned_data['opening_time']
				closing_time = test_form.cleaned_data['closing_time']
				time = get_time_difference(closing_time, opening_time)
				distributions = {
					"cutoff_mark": test_form.cleaned_data['cutoff_mark'],
					"max_mark": test_form.cleaned_data['max_mark'],
					"no_of_questions": test_form.cleaned_data['no_of_questions'],
					"time": time,
					"topics": topics,
				}
				test = test_form.save(commit=False)
				test.created_by = request.user
				test.modified_by = request.user
				test.distributions = distributions
				test.save()

				response["success"] = True
			else:
				# Collecting error messages
				error_messages = []
				errors = json.loads(test_form.errors.as_json())
				for x in errors:
					for y in errors[x]:
						error_messages.append(y['message'])
				
				# Sending response
				response["success"] = False
				response["errors"] = error_messages
				return JsonResponse(response)
		else:
			# Collecting error messages
			error_messages = []
			errors = json.loads(test_dist.errors.as_json())
			for x in errors:
				for y in errors[x]:
					error_messages.append(y['message'])
			
			# Sending response
			response["success"] = False
			response["errors"] = error_messages
			return JsonResponse(response)

		# Sending response
		context = {}
		batches = Batch.objects.filter(exam_category__subjects=subject)
		context['batches'] = batches
		context['test_form'] = TestForm
		TopicDistributionFormSet = formset_factory(TopicDistributionForm)
		context['test_topic_form'] = TopicDistributionFormSet(form_kwargs={'request': request})
		tests = []
		test_objs = Test.objects.all()
		topic_ids = list(Topic.objects.filter(subject=subject).values_list('id', flat=True))
		for test_obj in test_objs:
			for topic_dist in test_obj.distributions['topics']:
				if topic_dist['topic_id'] in topic_ids:
					tests.append(test_obj)
					break
		context['tests'] = tests

		response['template'] = render_to_string('tests/faculty/tests.html', context, request=request)
		return JsonResponse(response)