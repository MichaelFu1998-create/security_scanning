def template_to_filepath(template, metadata, template_patterns=None):
	"""Create directory structure and file name based on metadata template.

	Parameters:
		template (str): A filepath which can include template patterns as defined by :param template_patterns:.

		metadata (dict): A metadata dict.

		template_patterns (dict): A dict of ``pattern: field`` pairs used to replace patterns with metadata field values.
			Default: :const TEMPLATE_PATTERNS:

	Returns:
		A filepath.
	"""

	if template_patterns is None:
		template_patterns = TEMPLATE_PATTERNS

	metadata = metadata if isinstance(metadata, dict) else _mutagen_fields_to_single_value(metadata)
	assert isinstance(metadata, dict)

	suggested_filename = get_suggested_filename(metadata).replace('.mp3', '')

	if template == os.getcwd() or template == '%suggested%':
		filepath = suggested_filename
	else:
		t = template.replace('%suggested%', suggested_filename)
		filepath = _replace_template_patterns(t, metadata, template_patterns)

	return filepath