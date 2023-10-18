def _check_field_value(field_value, pattern):
	"""Check a song metadata field value for a pattern."""

	if isinstance(field_value, list):
		return any(re.search(pattern, str(value), re.I) for value in field_value)
	else:
		return re.search(pattern, str(field_value), re.I)