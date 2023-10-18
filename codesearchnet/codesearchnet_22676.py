def __get_numbered_paths(filepath):
	"""Append numbers in sequential order to the filename or folder name
	Numbers should be appended before the extension on a filename."""
	format = '%s (%%d)%s' % splitext_files_only(filepath)
	return map(lambda n: format % n, itertools.count(1))