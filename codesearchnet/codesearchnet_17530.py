def filter_local_songs(filepaths, include_filters=None, exclude_filters=None, all_includes=False, all_excludes=False):
	"""Match a local file against a set of metadata filters.

	Parameters:
		filepaths (list): Filepaths to filter.

		include_filters (list): A list of ``(field, pattern)`` tuples.
			Fields are any valid mutagen metadata fields.
			Patterns are Python regex patterns.
			Local songs are filtered out if the given metadata field values don't match any of the given patterns.

		exclude_filters (list): A list of ``(field, pattern)`` tuples.
			Fields are any valid mutagen metadata fields.
			Patterns are Python regex patterns.
			Local songs are filtered out if the given metadata field values match any of the given patterns.

		all_includes (bool): If ``True``, all include_filters criteria must match to include a song.

		all_excludes (bool): If ``True``, all exclude_filters criteria must match to exclude a song.

	Returns:
		A list of local song filepaths matching criteria and
		a list of local song filepaths filtered out using filter criteria.
		Invalid music files are also filtered out.
		::

			(matched, filtered)
	"""

	matched_songs = []
	filtered_songs = []

	for filepath in filepaths:
		try:
			song = _get_mutagen_metadata(filepath)
		except mutagen.MutagenError:
			filtered_songs.append(filepath)
		else:
			if include_filters or exclude_filters:
				if _check_filters(
						song, include_filters=include_filters, exclude_filters=exclude_filters,
						all_includes=all_includes, all_excludes=all_excludes):
					matched_songs.append(filepath)
				else:
					filtered_songs.append(filepath)
			else:
				matched_songs.append(filepath)

	return matched_songs, filtered_songs