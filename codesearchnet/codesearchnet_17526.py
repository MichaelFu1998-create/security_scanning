def exclude_filepaths(filepaths, exclude_patterns=None):
	"""Exclude file paths based on regex patterns.

	Parameters:
		filepaths (list or str): Filepath(s) to check.

		exclude_patterns (list): Python regex patterns to check filepaths against.

	Returns:
		A list of filepaths to include and a list of filepaths to exclude.
	"""

	if not exclude_patterns:
		return filepaths, []

	exclude_re = re.compile("|".join(pattern for pattern in exclude_patterns))

	included_songs = []
	excluded_songs = []

	for filepath in filepaths:
		if exclude_patterns and exclude_re.search(filepath):
			excluded_songs.append(filepath)
		else:
			included_songs.append(filepath)

	return included_songs, excluded_songs