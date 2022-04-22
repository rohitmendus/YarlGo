def role_processor(request):
	if request.user.is_authenticated:
		return {"user_role": list(request.user.roles.all())[0]}
	else:
		return {"user_role": False}