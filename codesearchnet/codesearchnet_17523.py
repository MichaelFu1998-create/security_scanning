def _normalize_metadata(metadata):
	"""Normalize metadata to improve match accuracy."""

	metadata = str(metadata)
	metadata = metadata.lower()

	metadata = re.sub(r'\/\s*\d+', '', metadata)  # Remove "/<totaltracks>" from track number.
	metadata = re.sub(r'^0+([0-9]+)', r'\1', metadata)  # Remove leading zero(s) from track number.
	metadata = re.sub(r'^\d+\.+', '', metadata)  # Remove dots from track number.
	metadata = re.sub(r'[^\w\s]', '', metadata)  # Remove any non-words.
	metadata = re.sub(r'\s+', ' ', metadata)  # Reduce multiple spaces to a single space.
	metadata = re.sub(r'^\s+', '', metadata)  # Remove leading space.
	metadata = re.sub(r'\s+$', '', metadata)  # Remove trailing space.
	metadata = re.sub(r'^the\s+', '', metadata, re.I)  # Remove leading "the".

	return metadata