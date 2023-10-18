def _check_filters(song, include_filters=None, exclude_filters=None, all_includes=False, all_excludes=False):
	"""Check a song metadata dict against a set of metadata filters."""

	include = True

	if include_filters:
		if all_includes:
			if not all(field in song and _check_field_value(song[field], pattern) for field, pattern in include_filters):
				include = False
		else:
			if not any(field in song and _check_field_value(song[field], pattern) for field, pattern in include_filters):
				include = False

	if exclude_filters:
		if all_excludes:
			if all(field in song and _check_field_value(song[field], pattern) for field, pattern in exclude_filters):
				include = False
		else:
			if any(field in song and _check_field_value(song[field], pattern) for field, pattern in exclude_filters):
				include = False

	return include