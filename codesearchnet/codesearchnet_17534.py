def get_local_songs(
			filepaths, include_filters=None, exclude_filters=None, all_includes=False, all_excludes=False,
			exclude_patterns=None, max_depth=float('inf')):
		"""Load songs from local filepaths.

		Parameters:
			filepaths (list or str): Filepath(s) to search for music files.

			include_filters (list): A list of ``(field, pattern)`` tuples.
				Fields are any valid mutagen metadata fields. Patterns are Python regex patterns.
				Local songs are filtered out if the given metadata field values don't match any of the given patterns.

			exclude_filters (list): A list of ``(field, pattern)`` tuples.
				Fields are any valid mutagen metadata fields. Patterns are Python regex patterns.
				Local songs are filtered out if the given metadata field values match any of the given patterns.

			all_includes (bool): If ``True``, all include_filters criteria must match to include a song.

			all_excludes (bool): If ``True``, all exclude_filters criteria must match to exclude a song.

			exclude_patterns (list or str): Pattern(s) to exclude.
				Patterns are Python regex patterns.
				Filepaths are excluded if they match any of the exclude patterns.

			max_depth (int): The depth in the directory tree to walk.
				A depth of '0' limits the walk to the top directory.
				Default: No limit.

		Returns:
			A list of local song filepaths matching criteria,
			a list of local song filepaths filtered out using filter criteria,
			and a list of local song filepaths excluded using exclusion criteria.

		"""

		logger.info("Loading local songs...")

		supported_filepaths = get_supported_filepaths(filepaths, SUPPORTED_SONG_FORMATS, max_depth=max_depth)

		included_songs, excluded_songs = exclude_filepaths(supported_filepaths, exclude_patterns=exclude_patterns)

		matched_songs, filtered_songs = filter_local_songs(
			included_songs, include_filters=include_filters, exclude_filters=exclude_filters,
			all_includes=all_includes, all_excludes=all_excludes
		)

		logger.info("Excluded {0} local songs".format(len(excluded_songs)))
		logger.info("Filtered {0} local songs".format(len(filtered_songs)))
		logger.info("Loaded {0} local songs".format(len(matched_songs)))

		return matched_songs, filtered_songs, excluded_songs