# Models
from django.contrib.auth.models import User
from subjects.models import Topic, Subject
from batches.models import Batch
from .models import Option, Question, Test, UserTest, UserQuestion
# Forms
from .forms import TopicDistributionForm, TestForm, QuestionEditorForm
from django.forms import formset_factory
# CBS Views
from django.views import View
# Mixins and decorators
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from accounts.mixins import FacultyRedirectMixin, StudentRedirectMixin
# Response objects
import mimetypes, os, openpyxl, json, datetime
from django.template.loader import render_to_string
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator, EmptyPage

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
	context['test_form'] = TestForm(request=request)
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
		# question = request.POST.get('question')
		form = QuestionEditorForm(request.POST)
		if form.is_valid():
			question = form.cleaned_data.get('question')
		else:
			# Sending response
			response1 = render_to_string(self.submit_response, {'success': False, 
				'errors': ['Question is invalid']})
			response2 = render_to_string(self.table, {'questions': Question.objects.filter(topic__subject=subject),
				'topics': Topic.objects.filter(subject=subject)})
			response = {
				'response1': response1, 'response2': response2
			}
			return JsonResponse(response)
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
		context = {'topics': Topic.objects.filter(subject=subject),
				'question_form': QuestionEditorForm}
		return render(request, 'tests/faculty/create_question.html', context)

class DownloadQuestionTempView(LoginRequiredMixin, FacultyRedirectMixin, View):
	def get(self, request):
		subject = Subject.objects.get(id=request.session['subject_id'])
		# Getting file path
		filename= "question_template.xlsx"
		BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
		filepath = BASE_DIR + '/templates/tests/faculty/' + filename

		# Loading the excel file
		wb = openpyxl.load_workbook(filepath)
		ws = wb['question']
		ws_topics = wb['topics']

		#Removing existing data downs if any
		toRemove = []
		for validation in ws.data_validations.dataValidation:
			if validation.__contains__('B2'):
				toRemove.append(validation)
		for rmValidation in toRemove:
			ws.data_validations.dataValidation.remove(rmValidation)

		#Adding new drop downs
		topic_names = Topic.objects.filter(subject=subject).values_list('name', flat=True)
		if len(topic_names) == 0:
			return redirect('/faculty')

		c = 1
		for topic in topic_names:
			c += 1
			ws_topics['A'+str(c)] = topic
		topics_len = len(topic_names)+1
		dv_topic = openpyxl.worksheet.datavalidation.DataValidation(type="list", formula1="{0}!$A$2:$A${1}".format(openpyxl.utils.quote_sheetname('topics'), topics_len))
		dv_answer = openpyxl.worksheet.datavalidation.DataValidation(type="list", formula1='"option 1,option 2,option 3,option 4"')
		ws.add_data_validation(dv_topic)
		dv_topic.add('B2:B100')
		ws.add_data_validation(dv_answer)
		dv_answer.add('G2:G100')

		ws_topics.sheet_state = "hidden"
		wb.save(filepath)

		#Sending the file as response
		path = open(filepath, 'rb')
		mime_type, _ = mimetypes.guess_type(filepath)
		response = HttpResponse(path, content_type=mime_type)
		response['Content-Disposition'] = "attachment; filename=%s" % filename
		return response

class UploadQuestionsView(LoginRequiredMixin, FacultyRedirectMixin, View):
	def post(self, request):
		subject = Subject.objects.get(id=self.request.session['subject_id'])
		file = request.FILES.get('question_file')

		wb = openpyxl.load_workbook(file)
		ws = wb['question']
		for x in range(2, 101):
			question = ws['A'+str(x)].value
			topic_name = ws['B'+str(x)].value
			answer_opt = ws['G'+str(x)].value
			option1_text = ws['C'+str(x)].value
			option2_text = ws['D'+str(x)].value
			option3_text = ws['E'+str(x)].value
			option4_text = ws['F'+str(x)].value

			if None not in [question, topic_name, answer_opt, option1_text, option2_text, option3_text, option4_text]:
				print([question, topic_name, answer_opt, option1_text, option2_text, option3_text, option4_text])
				topic = Topic.objects.get(name=topic_name)
				question_obj = Question(question=question, topic=topic, 
				created_by=request.user, modified_by=request.user)
				option1 = Option(text=option1_text)
				option2 = Option(text=option2_text)
				option3 = Option(text=option3_text)
				option4 = Option(text=option4_text)

				try:
					question_obj.full_clean(exclude=["answer"])
					option1.full_clean()
					option2.full_clean()
					option3.full_clean()
					option4.full_clean()
				except ValidationError as e:
					print(e)
				else:
					option1.save()
					option2.save()
					option3.save()
					option4.save()

					if answer_opt == "option 1":
						question_obj.answer = option1
					elif answer_opt == "option 2":
						question_obj.answer = option2
					elif answer_opt == "option 3":
						question_obj.answer = option3
					elif answer_opt == "option 4":
						question_obj.answer = option4

					question_obj.save()
					question_obj.options.add(option1, option2, option3, option4)
		return redirect("/faculty")

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
		response = render_to_string(self.template_name, {"question": question, 
			"topics": topics, 'question_form': QuestionEditorForm(instance=question)},
			request=request)
		return JsonResponse(response, safe=False)

	def post(self, request, question_id):
		question_obj = Question.objects.get(id=question_id)
		subject = Subject.objects.get(id=request.session['subject_id'])
		form = QuestionEditorForm(request.POST, instance=question_obj)
		if form.is_valid():
			question = form.cleaned_data.get('question')
		else:
			error_messages = []
			errors = json.loads(form.errors.as_json())
			for x in errors:
				for y in errors[x]:
					error_messages.append(y['message'])
			# Sending response
			response = {'success': False, 'errors': error_messages}
			return JsonResponse(response)
		topic_name = request.POST.get('edit_topic')
		topic = Topic.objects.get(name=topic_name)
		answer_opt = request.POST.get('edit_answer')
		
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
			context = {'topics': Topic.objects.filter(subject=subject),
				'question_form': QuestionEditorForm}
			form_response = render_to_string('tests/faculty/create_question.html', context, request=request)
			response = {'success': True, 'table_response': table_response, 'form_response': form_response}
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
			test_form = TestForm(data=post_data, request=request)
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
		context['test_form'] = TestForm(request=request)
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
		context['test_form'] = TestForm(instance=test, request=request)
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
		context['test_form'] = TestForm(instance=test, request=request)
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
			test_form = TestForm(data=post_data, instance=instance, request=request)
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
		context['test_form'] = TestForm(request=request)
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


# Student views
class QuestionBankView(LoginRequiredMixin, StudentRedirectMixin, View):
	template_name = "tests/student/question_bank.html"

	def get(self, request, topic_id):
		batch_id = request.session['batch_id']
		batch = Batch.objects.get(id=batch_id)
		topic = Topic.objects.get(id=topic_id)
		current_time = datetime.datetime.now().time()
		subjects = Subject.objects.filter(subject_timings__opening_time__lte=current_time, 
			subject_timings__closing_time__gte=current_time)
		if subjects.exists():
			for subject in subjects:
				if subject.exam_categories.filter(batches=batch) and topic.subject == subject:
					questions = Question.objects.filter(topic_id=topic_id)
					if len(questions) < 1:
						return redirect(f'/batches/batch/{batch_id}/')
					p = Paginator(questions, 10)
					page_num = request.GET.get('page')
					page = p.get_page(page_num)
					context = {'questions': page}
					return render(request, self.template_name, context)
		return redirect('/unauthorized')


class TestPromptView(LoginRequiredMixin, StudentRedirectMixin, View):
	template_name = 'tests/student/test_prompt.html'

	def get(self, request, test_id):
		test = Test.objects.get(id=test_id)

		if test.is_open != True:
			return redirect('/unauthorized')
		if test.test_taken(request.user):
			return redirect('/unauthorized')

		request.session['test_id'] = test_id
		topics_dist = test.distributions['topics']
		topics = []
		for topic_dist in topics_dist:
			topic = Topic.objects.get(id=topic_dist['topic_id'])
			percentage = (topic_dist['max_mark']/test.max_mark) * 100
			obj = {'topic': topic, 'percentage': percentage}
			topics.append(obj)

		batch_id = request.session['batch_id']
		return render(request, self.template_name, {'test': test, 'topics': topics, 'batch_id': batch_id})


class TakeTestView(LoginRequiredMixin, StudentRedirectMixin, View):
	template_name = 'tests/student/take_test.html'

	def get(self, request):
		test = Test.objects.get(id=request.session['test_id'])
		if test.is_open != True:
			return redirect('/unauthorized')
		if test.test_taken(request.user):
			return redirect('/unauthorized')

		if 'test_status' not in request.session or request.session['test_status'] != 0:
			request.session['test_started_on'] = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
			request.session['test_status'] = 0
			test_id = request.session['test_id']
			test = Test.objects.get(id=test_id)

			topics_dist = test.distributions['topics']
			questions = []
			user_questions = []
			for topic_dist in topics_dist:
				topic = Topic.objects.get(id=topic_dist['topic_id'])
				num = topic_dist['no_of_questions']
				question_set = Question.objects.filter(topic=topic).order_by('?')[:num]
				for question in question_set:
					obj1 = {'question_id': question.id, 'answered': False, 'marked': False,
						'option_choosen': None, 'started_on': None, 'finished_on': None}
					obj2 = {'id': question.id, 'question': question.question}
					c = 1
					for opt in question.options.all():
						key1 = f'option{c}'
						key2 = f'option{c}_id'
						obj2[key1] = opt.text
						obj2[key2] = opt.id
						c+=1

					questions.append(obj2)
					user_questions.append(obj1)

			request.session['questions'] = questions
			request.session['user_questions'] = user_questions
		page_num = request.GET.get('question')
		if page_num != None:
			if request.session['user_questions'][int(page_num)-1]['started_on'] == None:
				request.session['user_questions'][int(page_num)-1]['started_on'] = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
		else:
			request.session['user_questions'][0]['started_on'] = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
		request.session.modified = True
		p = Paginator(request.session['questions'], 1)
		page = p.get_page(page_num)
		context = {'questions': page}
		return render(request, self.template_name, context)

@csrf_exempt
def select_answer(request):
	if request.method == "POST":
		question_no = int(request.POST.get('question_no'))-1
		question_id = int(request.POST.get('question_id'))
		option_choosen = int(request.POST.get('option_choosen'))
		if request.session['user_questions'][question_no]['question_id'] == question_id:
			request.session['user_questions'][question_no]['finished_on'] = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
			request.session['user_questions'][question_no]['answered'] = True
			request.session['user_questions'][question_no]['option_choosen'] = option_choosen
			request.session.modified = True
		return JsonResponse('Success', safe=False)

@csrf_exempt
def clear_answer(request):
	if request.method == "POST":
		question_no = int(request.POST.get('question_no'))-1
		question_id = int(request.POST.get('question_id'))
		if request.session['user_questions'][question_no]['question_id'] == question_id:
			request.session['user_questions'][question_no]['finished_on'] = None
			request.session['user_questions'][question_no]['answered'] = False
			request.session['user_questions'][question_no]['option_choosen'] = None
			request.session.modified = True
		return JsonResponse('Success', safe=False)

@csrf_exempt
def mark_question(request):
	if request.method == "POST":
		question_no = int(request.POST.get('question_no'))-1
		question_id = int(request.POST.get('question_id'))
		mark = request.POST.get('mark')
		if request.session['user_questions'][question_no]['question_id'] == question_id:
			if mark == "true":
				request.session['user_questions'][question_no]['marked'] = True
			else:
				request.session['user_questions'][question_no]['marked'] = False
			request.session.modified = True
		return JsonResponse('Success', safe=False)


def get_test_info(request):
	if request.method == "GET":
		c = 0
		for i in request.session['user_questions']:
			if i['answered'] == False:
				c+=1
		if c == 0:
			return JsonResponse('All the questions have been answered!', safe=False)
		else:
			message = f'You have {c} unanswered questions!'
			return JsonResponse(message, safe=False)

def submit_test(request):
	if request.method == "POST":
		test = Test.objects.get(id=request.session['test_id'])
		marks_gained = 0
		for i in request.session['user_questions']:
			question = Question.objects.get(id=i['question_id'])
			if i['option_choosen'] != None:
				option_choosen = Option.objects.get(id=i['option_choosen'])
			else:
				option_choosen = None
			if i['started_on'] == None or i['finished_on'] == None:
				time_taken = None
			else:
				started_on = datetime.datetime.strptime(i['started_on'], "%m/%d/%Y, %H:%M:%S")
				finished_on = datetime.datetime.strptime(i['finished_on'], "%m/%d/%Y, %H:%M:%S")
				time_taken = finished_on - started_on
			if i['answered']:
				if question.answer == option_choosen:
					state = 1
					marks_gained += 1
				else:
					state = 0
			else:
				state = 2
			UserQuestion.objects.create(question=question, option_choosen=option_choosen,
				time_taken=time_taken, state=state, test=test, user=request.user)

		test_started_on = datetime.datetime.strptime(request.session['test_started_on'], "%m/%d/%Y, %H:%M:%S")
		test_completed_on = datetime.datetime.now()
		UserTest.objects.create(test=test, user=request.user, marks_gained=marks_gained, started_on=test_started_on,
			completed_on=test_completed_on)
		del request.session['questions']
		del request.session['user_questions']
		del request.session['test_id']
		del request.session['test_status']
		del request.session['test_started_on']
		request.session.modified = True
		batch_id = request.session['batch_id']
		return redirect(f'/batches/batch/{batch_id}/')


class ReviewAnswersView(View):
	template_name = "tests/student/review_answers.html"

	def get(self, request, test_id):
		test_stats = UserTest.objects.get(test_id=test_id, user=request.user)

		questions = UserQuestion.objects.filter(test_id=test_id, user=request.user)
		
		page_num = request.GET.get('page')
		p = Paginator(questions, 10)
		page = p.get_page(page_num)
		context = {'test_stats': test_stats, 'questions': page}
		return render(request, self.template_name, context)


