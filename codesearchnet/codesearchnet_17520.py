def _get_mutagen_metadata(filepath):
	"""Get mutagen metadata dict from a file."""

	try:
		metadata = mutagen.File(filepath, easy=True)
	except mutagen.MutagenError:
		logger.warning("Can't load {} as music file.".format(filepath))
		raise

	return metadata