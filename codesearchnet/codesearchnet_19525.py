def queryString_required(strList):
	"""	An decorator checking whether queryString key is valid or not
	Args:
		str: allowed queryString key

	Returns:
		if contains invalid queryString key, it will raise exception.
	"""
	def _dec(function):
		@wraps(function)
		def _wrap(request, *args, **kwargs):
			for i in strList:
				if i not in request.GET:
					raise Http404("api does not exist")
			return function(request, *args, **kwargs)
		return _wrap
	return _dec