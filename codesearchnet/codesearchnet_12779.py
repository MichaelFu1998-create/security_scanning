def get_publication(context, id):
	"""
	Get a single publication.
	"""

	pbl = Publication.objects.filter(pk=int(id))

	if len(pbl) < 1:
		return ''

	pbl[0].links = pbl[0].customlink_set.all()
	pbl[0].files = pbl[0].customfile_set.all()

	return render_template(
		'publications/publication.html', context['request'], {'publication': pbl[0]})