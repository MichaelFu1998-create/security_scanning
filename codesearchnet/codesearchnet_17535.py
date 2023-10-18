def get_local_playlists(filepaths, exclude_patterns=None, max_depth=float('inf')):
		"""Load playlists from local filepaths.

		Parameters:
			filepaths (list or str): Filepath(s) to search for music files.

			exclude_patterns (list or str): Pattern(s) to exclude.
				Patterns are Python regex patterns.
				Filepaths are excluded if they match any of the exclude patterns.

			max_depth (int): The depth in the directory tree to walk.
				A depth of '0' limits the walk to the top directory.
				Default: No limit.

		Returns:
			A list of local playlist filepaths matching criteria
			and a list of local playlist filepaths excluded using exclusion criteria.
		"""

		logger.info("Loading local playlists...")

		included_playlists = []
		excluded_playlists = []

		supported_filepaths = get_supported_filepaths(filepaths, SUPPORTED_PLAYLIST_FORMATS, max_depth=max_depth)

		included_playlists, excluded_playlists = exclude_filepaths(supported_filepaths, exclude_patterns=exclude_patterns)

		logger.info("Excluded {0} local playlists".format(len(excluded_playlists)))
		logger.info("Loaded {0} local playlists".format(len(included_playlists)))

		return included_playlists, excluded_playlists