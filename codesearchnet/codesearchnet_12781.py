def tex_parse(string):
	"""
	Renders some basic TeX math to HTML.
	"""

	string = string.replace('{', '').replace('}', '')
	def tex_replace(match):
		return \
			sub(r'\^(\w)', r'<sup>\1</sup>',
			sub(r'\^\{(.*?)\}', r'<sup>\1</sup>',
			sub(r'\_(\w)', r'<sub>\1</sub>',
			sub(r'\_\{(.*?)\}', r'<sub>\1</sub>',
			sub(r'\\(' + GREEK_LETTERS + ')', r'&\1;', match.group(1))))))
	return mark_safe(sub(r'\$([^\$]*)\$', tex_replace, escape(string)))