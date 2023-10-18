def parse(string):
	"""
	Takes a string in BibTex format and returns a list of BibTex entries, where
	each entry is a dictionary containing the entries' key-value pairs.

	@type  string: string
	@param string: bibliography in BibTex format

	@rtype: list
	@return: a list of dictionaries representing a bibliography
	"""

	# bibliography
	bib = []

	# make sure we are dealing with unicode strings
	if not isinstance(string, six.text_type):
		string = string.decode('utf-8')

	# replace special characters
	for key, value in special_chars:
		string = string.replace(key, value)
	string = re.sub(r'\\[cuHvs]{?([a-zA-Z])}?', r'\1', string)

	# split into BibTex entries
	entries = re.findall(
		r'(?u)@(\w+)[ \t]?{[ \t]*([^,\s]*)[ \t]*,?\s*((?:[^=,\s]+\s*\=\s*(?:"[^"]*"|{(?:[^{}]*|{[^{}]*})*}|[^,}]*),?\s*?)+)\s*}',
		string)

	for entry in entries:
		# parse entry
		pairs = re.findall(r'(?u)([^=,\s]+)\s*\=\s*("[^"]*"|{(?:[^{}]*|{[^{}]*})*}|[^,]*)', entry[2])

		# add to bibliography
		bib.append({'type': entry[0].lower(), 'key': entry[1]})

		for key, value in pairs:
			# post-process key and value
			key = key.lower()
			if value and value[0] == '"' and value[-1] == '"':
				value = value[1:-1]
			if value and value[0] == '{' and value[-1] == '}':
				value = value[1:-1]
			if key not in ['booktitle', 'title']:
				value = value.replace('}', '').replace('{', '')
			else:
				if value.startswith('{') and value.endswith('}'):
					value = value[1:]
					value = value[:-1]
			value = value.strip()
			value = re.sub(r'\s+', ' ', value)

			# store pair in bibliography
			bib[-1][key] = value

	return bib