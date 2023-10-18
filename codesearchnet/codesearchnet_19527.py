def getJsonFromApi(view, request):
	"""Return json from querying Web Api

		Args:
			view: django view function.
			request: http request object got from django.
				
		Returns: json format dictionary
		"""
	jsonText = view(request)
	jsonText = json.loads(jsonText.content.decode('utf-8'))
	return jsonText