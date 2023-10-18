def insert_before_extension(filename, content):
	"""
	Given a filename and some content, insert the content just before
	the extension.

	>>> insert_before_extension('pages.pdf', '-old')
	'pages-old.pdf'
	"""
	parts = list(os.path.splitext(filename))
	parts[1:1] = [content]
	return ''.join(parts)