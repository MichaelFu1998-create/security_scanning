def get_google_songs(
		self, include_filters=None, exclude_filters=None, all_includes=False, all_excludes=False,
		uploaded=True, purchased=True):
		"""Create song list from user's Google Music library.

		Parameters:
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

			uploaded (bool): Include uploaded songs. Default: ``True``.

			purchased (bool): Include purchased songs. Default: ``True``.

		Returns:
			A list of Google Music song dicts matching criteria and
			a list of Google Music song dicts filtered out using filter criteria.
		"""

		if not uploaded and not purchased:
			raise ValueError("One or both of uploaded/purchased parameters must be True.")

		logger.info("Loading Google Music songs...")

		google_songs = []

		if uploaded:
			google_songs += self.api.get_uploaded_songs()

		if purchased:
			for song in self.api.get_purchased_songs():
				if song not in google_songs:
					google_songs.append(song)

		matched_songs, filtered_songs = filter_google_songs(
			google_songs, include_filters=include_filters, exclude_filters=exclude_filters,
			all_includes=all_includes, all_excludes=all_excludes
		)

		logger.info("Filtered {0} Google Music songs".format(len(filtered_songs)))
		logger.info("Loaded {0} Google Music songs".format(len(matched_songs)))

		return matched_songs, filtered_songs