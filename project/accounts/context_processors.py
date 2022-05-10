from batches.models import Batch
def custom_processor(request):
	context = {}
	try:
		user_role = list(request.user.roles.all())[0]
		if str(user_role) == "student":
			batches = Batch.objects.filter(students=request.user)
			context['batches'] = batches
	except:
		user_role = False
	context['user_role'] = user_role
	return context