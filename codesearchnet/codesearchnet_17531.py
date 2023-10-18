def get_suggested_filename(metadata):
	"""Generate a filename for a song based on metadata.

	Parameters:
		metadata (dict): A metadata dict.

	Returns:
		A filename.
	"""

	if metadata.get('title') and metadata.get('track_number'):
		suggested_filename = '{track_number:0>2} {title}'.format(**metadata)
	elif metadata.get('title') and metadata.get('trackNumber'):
		suggested_filename = '{trackNumber:0>2} {title}'.format(**metadata)
	elif metadata.get('title') and metadata.get('tracknumber'):
		suggested_filename = '{tracknumber:0>2} {title}'.format(**metadata)
	else:
		suggested_filename = '00 {}'.format(metadata.get('title', ''))

	return suggested_filename