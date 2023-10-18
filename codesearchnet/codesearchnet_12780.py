def get_publication_list(context, list, template='publications/publications.html'):
	"""
	Get a publication list.
	"""

	list = List.objects.filter(list__iexact=list)

	if not list:
		return ''

	list = list[0]
	publications = list.publication_set.all()
	publications = publications.order_by('-year', '-month', '-id')

	if not publications:
		return ''

	# load custom links and files
	populate(publications)

	return render_template(
		template, context['request'], {'list': list, 'publications': publications})