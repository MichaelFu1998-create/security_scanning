def get_publications(context, template='publications/publications.html'):
	"""
	Get all publications.
	"""

	types = Type.objects.filter(hidden=False)
	publications = Publication.objects.select_related()
	publications = publications.filter(external=False, type__in=types)
	publications = publications.order_by('-year', '-month', '-id')

	if not publications:
		return ''

	# load custom links and files
	populate(publications)

	return render_template(template, context['request'], {'publications': publications})