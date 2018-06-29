def name(request):
	name = request.session.get('name')
	return {'name': name}
