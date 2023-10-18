def get_local_playlist_songs(
		playlist, include_filters=None, exclude_filters=None,
		all_includes=False, all_excludes=False, exclude_patterns=None):
		"""Load songs from local playlist.

		Parameters:
			playlist (str): An M3U(8) playlist filepath.

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

		Returns:
			A list of local playlist song filepaths matching criteria,
			a list of local playlist song filepaths filtered out using filter criteria,
			and a list of local playlist song filepaths excluded using exclusion criteria.
		"""

		logger.info("Loading local playlist songs...")

		if os.name == 'nt' and CYGPATH_RE.match(playlist):
			playlist = convert_cygwin_path(playlist)

		filepaths = []
		base_filepath = os.path.dirname(os.path.abspath(playlist))

		with open(playlist) as local_playlist:
			for line in local_playlist.readlines():
				line = line.strip()

				if line.lower().endswith(SUPPORTED_SONG_FORMATS):
					path = line

					if not os.path.isabs(path):
						path = os.path.join(base_filepath, path)

					if os.path.isfile(path):
						filepaths.append(path)

		supported_filepaths = get_supported_filepaths(filepaths, SUPPORTED_SONG_FORMATS)

		included_songs, excluded_songs = exclude_filepaths(supported_filepaths, exclude_patterns=exclude_patterns)

		matched_songs, filtered_songs = filter_local_songs(
			included_songs, include_filters=include_filters, exclude_filters=exclude_filters,
			all_includes=all_includes, all_excludes=all_excludes
		)

		logger.info("Excluded {0} local playlist songs".format(len(excluded_songs)))
		logger.info("Filtered {0} local playlist songs".format(len(filtered_songs)))
		logger.info("Loaded {0} local playlist songs".format(len(matched_songs)))

		return matched_songs, filtered_songs, excluded_songs