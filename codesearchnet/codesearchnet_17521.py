def _mutagen_fields_to_single_value(metadata):
	"""Replace mutagen metadata field list values in mutagen tags with the first list value."""

	return dict((k, v[0]) for k, v in metadata.items() if v)