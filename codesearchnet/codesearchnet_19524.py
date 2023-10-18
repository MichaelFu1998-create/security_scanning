def date_proc(func):
	"""	An decorator checking whether date parameter is passing in or not. If not, default date value is all PTT data.
		Else, return PTT data with right date.
	Args:
		func: function you want to decorate.
		request: WSGI request parameter getten from django.

	Returns:
		date:
			a datetime variable, you can only give year, year + month or year + month + day, three type.
			The missing part would be assigned default value 1 (for month is Jan, for day is 1).
	"""
	@wraps(func)
	def wrapped(request, *args, **kwargs):
		if 'date' in request.GET and request.GET['date'] == '':
			raise Http404("api does not exist")
		elif 'date' not in request.GET:
			date = datetime.today()
			return func(request, date)
		else:
			date = tuple(int(intValue) for intValue in request.GET['date'].split('-'))
			if len(date) == 3:
				date = datetime(*date)
			elif len(date) == 2:
				date = datetime(*date, day = 1)
			else:
				date = datetime(*date, month = 1, day = 1)
			return func(request, date)
	return wrapped