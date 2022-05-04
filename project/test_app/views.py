# Models
from django.contrib.auth.models import User
from subjects.models import Topic, Subject
from .models import Option, Question
# CBS Views
# from django.views.generic.list import ListView
# from django.views.generic.edit import FormView, UpdateView
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
