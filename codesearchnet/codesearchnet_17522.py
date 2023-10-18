def _split_field_to_single_value(field):
	"""Convert number field values split by a '/' to a single number value."""

	split_field = re.match(r'(\d+)/\d+', field)

	return split_field.group(1) or field