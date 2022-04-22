def role_processor(request):
	try:
		return {"user_role": list(request.user.roles.all())[0]}
	except:
		return {"user_role": False}