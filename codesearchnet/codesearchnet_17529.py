def filter_google_songs(songs, include_filters=None, exclude_filters=None, all_includes=False, all_excludes=False):
	"""Match a Google Music song dict against a set of metadata filters.

	Parameters:
		songs (list): Google Music song dicts to filter.

		include_filters (list): A list of ``(field, pattern)`` tuples.
			Fields are any valid Google Music metadata field available to the Musicmanager client.
			Patterns are Python regex patterns.
			Google Music songs are filtered out if the given metadata field values don't match any of the given patterns.

		exclude_filters (list): A list of ``(field, pattern)`` tuples.
			Fields are any valid Google Music metadata field available to the Musicmanager client.
			Patterns are Python regex patterns.
			Google Music songs are filtered out if the given metadata field values match any of the given patterns.

		all_includes (bool): If ``True``, all include_filters criteria must match to include a song.

		all_excludes (bool): If ``True``, all exclude_filters criteria must match to exclude a song.

	Returns:
		A list of Google Music song dicts matching criteria and
		a list of Google Music song dicts filtered out using filter criteria.
		::

			(matched, filtered)
	"""

	matched_songs = []
	filtered_songs = []

	if include_filters or exclude_filters:
		for song in songs:
			if _check_filters(
					song, include_filters=include_filters, exclude_filters=exclude_filters,
					all_includes=all_includes, all_excludes=all_excludes):
				matched_songs.append(song)
			else:
				filtered_songs.append(song)
	else:
		matched_songs += songs

	return matched_songs, filtered_songs