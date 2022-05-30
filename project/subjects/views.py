# Models
from .models import Subject, FacultyRight, Right, Topic
from accounts.models import Role
from batches.models import Batch
from test_app.models import Question, Test
from django.contrib.auth.models import User
# Forms
from django.forms import formset_factory
from .forms import SubjectForm, TopicForm
from test_app.forms import TestForm, TopicDistributionForm, QuestionEditorForm
# CBS Views
from django.views.generic.list import ListView
from django.views.generic.edit import FormView, UpdateView
from django.views import View
# Mixins and decorators
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from accounts.mixins import AdminRedirectMixin, FacultyRedirectMixin
# Response objects
from django.shortcuts import render, redirect
import mimetypes, os, openpyxl, json, datetime
from django.template.loader import render_to_string
from django.http import JsonResponse, HttpResponse
from .utils import send_faculty_allocation_mail


# Admin Views.
@login_required
def get_subject_form(request):
	form = SubjectForm()
	faculties = Role.objects.filter(name="faculty").values_list('users__first_name', 'users__last_name', 'users__username', 'users__email')
	return render(request, 'subjects/admin/create_subject.html', {'form': SubjectForm(), 'faculties': faculties})

class AdminSubjectsView(LoginRequiredMixin, AdminRedirectMixin, ListView):
	template_name = "subjects/admin/subjects.html"
	model = Subject
	context_object_name = "subjects"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		faculties = Role.objects.filter(name="faculty").values_list('users__first_name', 'users__last_name', 'users__username', 'users__email')
		context.update({'form': SubjectForm(), 'faculties': faculties})
		return context

class CreateSubjectView(LoginRequiredMixin, AdminRedirectMixin, FormView):
	form_class = SubjectForm
	submit_response = "subjects/admin/create_subject_response.html"
	table = "subjects/admin/subject_list.html"

	def right_conflict(self):
		errors = ['The same user cannot have both rights examiner and staff.']
		# Sending response
		response1 = render_to_string(self.submit_response, {'success': False, 
			'errors': errors})
		faculties = Role.objects.filter(name="faculty").values_list('users__username', flat=True)
		response2 = render_to_string(self.table, {'subjects': Subject.objects.all(), 
			'faculties': faculties})
		response = {
			'response1': response1, 'response2': response2
		}
		return JsonResponse(response)

	def form_valid(self, form):
		examiners = self.request.POST.getlist('examiners')
		staff = self.request.POST.getlist('staff')
		# Saving subject
		subject = form.save(commit=False)
		subject.created_by = self.request.user
		subject.modified_by = self.request.user
		subject.save()

		mail_list = []
		# Adding examiners
		examiner_right = Right.objects.get(name="examiner")
		for i in examiners:
			if i in staff:
				return self.right_conflict()
			user = 	User.objects.get(username=i)
			FacultyRight.objects.create(user=user, subject=subject, right=examiner_right)
			mail_obj = {'name': user.profile.full_name, 'email': user.email, 
			'role': 'examiner', 'subject': subject.name}
			mail_list.append(mail_obj)

		# Adding staff
		staff_right = Right.objects.get(name="staff")
		for i in staff:
			user = 	User.objects.get(username=i)
			FacultyRight.objects.create(user=user, subject=subject, right=staff_right)
			mail_obj = {'name': user.profile.full_name, 'email': user.email, 
			'role': 'staff', 'subject': subject.name}
			mail_list.append(mail_obj)

		# Sending faculty allocation mail
		send_faculty_allocation_mail(mail_list)

		# Sending response
		response1 = render_to_string(self.submit_response, {'success': True})
		faculties = Role.objects.filter(name="faculty").values_list('users__username', flat=True)
		response2 = render_to_string(self.table, {'subjects': Subject.objects.all(), 
			'faculties': faculties})
		response = {
			'response1': response1, 'response2': response2
		}
		return JsonResponse(response)

	def form_invalid(self, form):
		# Collecting error messages
		error_messages = []
		errors = json.loads(form.errors.as_json())
		for x in errors:
			for y in errors[x]:
				error_messages.append(y['message'])
		
		# Sending response
		response1 = render_to_string(self.submit_response, {'success': False, 
			'errors': error_messages})
		faculties = Role.objects.filter(name="faculty").values_list('users__username', flat=True)
		response2 = render_to_string(self.table, {'subjects': Subject.objects.all(), 
			'faculties': faculties})
		response = {
			'response1': response1, 'response2': response2
		}
		return JsonResponse(response)

class DeleteSubjectView(LoginRequiredMixin, AdminRedirectMixin, View):
	table = 'subjects/admin/subject_list.html'
	def post(self, request, subject_id):
		# Deleting subject
		subject = Subject.objects.get(id=subject_id)
		subject.delete()

		# Reponse
		faculties = Role.objects.filter(name="faculty").values_list('users__username', flat=True)
		table_response = render_to_string(self.table, {'subjects': Subject.objects.all(), 
			'faculties': faculties})
		return JsonResponse(table_response, safe=False)

class EditSubjectView(LoginRequiredMixin, AdminRedirectMixin, UpdateView):
	template_name = 'subjects/admin/edit_subject.html'
	model = Subject
	form_class = SubjectForm
	table = 'subjects/admin/subject_list.html'
	pk_url_kwarg = "subject_id"

	def right_conflict(self):
		errors = ['The same user cannot have both rights examiner and staff.']
		response = {'success': False, 'errors': errors}
		return JsonResponse(response)


	def form_valid(self, form):
		examiners = self.request.POST.getlist('edit-examiners')
		staff = self.request.POST.getlist('edit-staff')
		# Saving subject
		subject = form.save(commit=False)
		subject.modified_by = self.request.user
		subject.save()

		# Removing examiners
		examiner_right = Right.objects.get(name="examiner")
		examiner_rights = list(FacultyRight.objects.filter(subject=subject, right=examiner_right).values_list('user__username', flat=True))

		for username in examiner_rights:
			if username not in examiners:
				FacultyRight.objects.get(right=examiner_right, user__username=username, subject=subject).delete()

		mail_list = []
		# Adding examiners
		for i in examiners:
			if i in staff:
				return self.right_conflict()
			user = 	User.objects.get(username=i)
			faculty_right, created = FacultyRight.objects.get_or_create(user=user, subject=subject, right=examiner_right)
			if created:
				mail_obj = {'name': user.profile.full_name, 'email': user.email, 
				'role': 'examiner', 'subject': subject.name}
				mail_list.append(mail_obj)

		# Removing examiners
		staff_right = Right.objects.get(name="staff")
		staff_rights = list(FacultyRight.objects.filter(subject=subject, right=staff_right).values_list('user__username', flat=True))

		for username in staff_rights:
			if username not in staff:
				FacultyRight.objects.get(right=staff_right, user__username=username, subject=subject).delete()
		
		# Adding staff
		for i in staff:
			user = 	User.objects.get(username=i)
			faculty_right, created = FacultyRight.objects.get_or_create(user=user, subject=subject, right=staff_right)
			if created:
				mail_obj = {'name': user.profile.full_name, 'email': user.email, 
				'role': 'staff', 'subject': subject.name}
				mail_list.append(mail_obj)

		# Sending faculty allocation mail
		send_faculty_allocation_mail(mail_list)

		# Reponse
		faculties = Role.objects.filter(name="faculty").values_list('users__username', flat=True)
		table_response = render_to_string(self.table, {'subjects': Subject.objects.all(), 
			'faculties': faculties})
		response = {'success': True, 'table_response': table_response}
		return JsonResponse(response)

	def form_invalid(self, form):
		error_messages = []
		errors = json.loads(form.errors.as_json())
		for x in errors:
			for y in errors[x]:
				error_messages.append(y['message'])
		
		# Reponse
		response = {'success': False, 'errors': error_messages}
		return JsonResponse(response)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		faculties = Role.objects.filter(name="faculty").values_list('users__first_name', 'users__last_name', 'users__username', 'users__email')
		examiners = FacultyRight.objects.filter(right__name="examiner", subject=self.object).values_list('user__username', flat=True)
		staff = FacultyRight.objects.filter(right__name="staff", subject=self.object).values_list('user__username', flat=True)
		context.update({'faculties': faculties, 'examiners': examiners, 'staff': staff})
		return context




# Faculty Views
@login_required
def store_subject(request):
	request.session['subject_id'] = request.GET.get('subject_id')
	return JsonResponse('Stored', safe=False)

@login_required
def get_topic_form(request):
	form = TopicForm()
	return render(request, 'subjects/faculty/create_topic.html', {'form_topic': form})

@login_required
def get_question_date_graph(request):
	if request.method == "GET":
		subject = Subject.objects.get(id=request.session['subject_id'])

		from_date = request.GET.get('from_date')
		from_date = datetime.datetime.strptime(from_date, "%m/%d/%Y")
		to_date = from_date.date() + datetime.timedelta(days=6)

		question_date_set = {}
		for c in range(7):
			date = from_date + datetime.timedelta(days=c)
			date = date.strftime("%d %b")
			question_date_set[date] = 0

		for i in Question.objects.filter(topic__subject=subject, 
			date_created__date__gte=from_date, 
			date_created__date__lte=to_date).order_by('date_created'):
			date = i.date_created.strftime("%d %b")
			question_date_set[date] += 1

		labels = []
		data = []
		for i in question_date_set:
			labels.append(i)
			data.append(question_date_set[i])
		response = {'labels': labels, 'data': data}
		return JsonResponse(response)

class FacultyAllotmentView(LoginRequiredMixin, FacultyRedirectMixin, ListView):
	context_object_name = "allotments"
	template_name = "subjects/faculty/allotments.html"

	def get_queryset(self):
		return FacultyRight.objects.filter(user=self.request.user)

class FacultyTemplateView(LoginRequiredMixin, FacultyRedirectMixin, View):
	template_name = "subjects/faculty/faculty.html"
	def get(self, request):
		subject = Subject.objects.get(id=request.session['subject_id'])

		is_examiner = self.request.user.subject_rights.filter(subject=subject, right__name="examiner").exists()
		context = {'is_examiner': is_examiner, 
			'topics': Topic.objects.filter(subject=subject), 'subject': subject
		}
		if is_examiner:
			context['form_topic'] = TopicForm

		batches = Batch.objects.filter(exam_category__subjects=subject)
		context['batches'] = batches
		questions = Question.objects.filter(topic__subject=subject)
		context['questions'] = questions
		context['question_form'] = QuestionEditorForm
		
		context['test_form'] = TestForm(request)
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


		from_date = datetime.datetime.now().date() - datetime.timedelta(days=6)
		question_date_set = {}
		for c in range(7):
			date = from_date + datetime.timedelta(days=c)
			date = date.strftime("%d %b")
			question_date_set[date] = 0
		for i in Question.objects.filter(topic__subject=subject, 
			date_created__date__gte=from_date).order_by('date_created'):
			date = i.date_created.strftime("%d %b")
			question_date_set[date] += 1
		context['question_date'] = question_date_set


		faculty_question_set = []
		for i in FacultyRight.objects.filter(subject=subject):
			faculty = f'{i.user.first_name} {i.user.last_name}'
			obj = {'faculty': faculty, 'email': i.user.email,
			'no_of_questions': i.user.questions_created.filter(
				topic__subject=subject).count()}
			faculty_question_set.append(obj)

		context['faculty_question_set'] = faculty_question_set


		return render(request, self.template_name, context)

class CreateTopicView(LoginRequiredMixin, FacultyRedirectMixin, FormView):
	form_class = TopicForm
	submit_response = "subjects/faculty/create_topic_response.html"
	table = "subjects/faculty/topic_list.html"

	def form_valid(self, form):
		subject = Subject.objects.get(id=self.request.session['subject_id'])
		# Saving topic
		topic = form.save(commit=False)
		topic.created_by = self.request.user
		topic.modified_by = self.request.user
		topic.subject = subject
		topic.save()

		# Sending response
		response1 = render_to_string(self.submit_response, {'success': True})
		response2 = render_to_string(self.table, {'topics': Topic.objects.filter(subject=subject)})
		response = {
			'response1': response1, 'response2': response2
		}
		return JsonResponse(response)

	def form_invalid(self, form):
		subject = Subject.objects.get(id=self.request.session['subject_id'])
		# Collecting error messages
		error_messages = []
		errors = json.loads(form.errors.as_json())
		for x in errors:
			for y in errors[x]:
				error_messages.append(y['message'])
		
		# Sending response
		response1 = render_to_string(self.submit_response, {'success': False, 
			'errors': error_messages})
		response2 = render_to_string(self.table, {'topics': Topic.objects.filter(subject=subject)})
		response = {
			'response1': response1, 'response2': response2
		}
		return JsonResponse(response)

class DeleteTopicView(LoginRequiredMixin, FacultyRedirectMixin, View):
	table = 'subjects/faculty/topic_list.html'
	def post(self, request, topic_id):
		subject = Subject.objects.get(id=self.request.session['subject_id'])
		# Deleting topic
		topic = Topic.objects.get(id=topic_id)
		topic.delete()

		# Reponse
		table_response = render_to_string(self.table, {'topics': Topic.objects.filter(subject=subject)})
		return JsonResponse(table_response, safe=False)

class DeleteTopicQuestionsView(LoginRequiredMixin, FacultyRedirectMixin, View):
	table = 'subjects/faculty/topic_list.html'
	def post(self, request, topic_id):
		subject = Subject.objects.get(id=self.request.session['subject_id'])
		# Deleting all the questions in a topic
		topic = Topic.objects.get(id=topic_id)
		questions = Question.objects.filter(topic=topic)
		for question in questions:
			question.delete()

		# Reponse
		table_response = render_to_string(self.table, {'topics': Topic.objects.filter(subject=subject)})
		return JsonResponse(table_response, safe=False)

class EditTopicView(LoginRequiredMixin, FacultyRedirectMixin, UpdateView):
	template_name = 'subjects/faculty/edit_topic.html'
	model = Topic
	form_class = TopicForm
	table = 'subjects/faculty/topic_list.html'
	pk_url_kwarg = "topic_id"

	def form_valid(self, form):
		subject = Subject.objects.get(id=self.request.session['subject_id'])
		# Saving topic
		topic = form.save(commit=False)
		topic.modified_by = self.request.user
		topic.subject = subject
		topic.save()

		# Reponse
		table_response = render_to_string(self.table, {'topics': Topic.objects.filter(subject=subject)})
		response = {'success': True, 'table_response': table_response}
		return JsonResponse(response)

	def form_invalid(self, form):
		error_messages = []
		errors = json.loads(form.errors.as_json())
		for x in errors:
			for y in errors[x]:
				error_messages.append(y['message'])
		
		# Reponse
		response = {'success': False, 'errors': error_messages}
		return JsonResponse(response)

class DownloadTopicTempView(LoginRequiredMixin, FacultyRedirectMixin, View):
	def get(self, request):
		# Getting file path
		filename= "topic_template.xlsx"
		BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
		filepath = BASE_DIR + '/templates/subjects/faculty/' + filename

		#Sending the file as response
		path = open(filepath, 'rb')
		mime_type, _ = mimetypes.guess_type(filepath)
		response = HttpResponse(path, content_type=mime_type)
		response['Content-Disposition'] = "attachment; filename=%s" % filename
		return response

class UploadTopicsView(LoginRequiredMixin, FacultyRedirectMixin, View):
	def post(self, request):
		subject = Subject.objects.get(id=self.request.session['subject_id'])
		file = request.FILES.get('topic_file')

		errors= []
		wb = openpyxl.load_workbook(file)
		ws = wb['topic']
		for x in range(2, 101):
			name = ws['A'+str(x)].value
			description = ws['B'+str(x)].value
			topic = Topic(name=name, description=description, subject=subject, created_by=request.user, modified_by=request.user)
			try:
				topic.full_clean()
				topic.save()
			except:
				pass
			
		return redirect("/faculty")