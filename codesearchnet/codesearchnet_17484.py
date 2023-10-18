def get_google_playlist_songs(self, playlist, include_filters=None, exclude_filters=None, all_includes=False, all_excludes=False):
		"""Create song list from a user-generated Google Music playlist.

		Parameters:
			playlist (str): Name or ID of Google Music playlist. Names are case-sensitive.
				Google allows multiple playlists with the same name.
				If multiple playlists have the same name, the first one encountered is used.

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
			A list of Google Music song dicts in the playlist matching criteria and
			a list of Google Music song dicts in the playlist filtered out using filter criteria.
		"""

		logger.info("Loading Google Music playlist songs...")

		google_playlist = self.get_google_playlist(playlist)

		if not google_playlist:
			return [], []

		playlist_song_ids = [track['trackId'] for track in google_playlist['tracks']]
		playlist_songs = [song for song in self.api.get_all_songs() if song['id'] in playlist_song_ids]

		matched_songs, filtered_songs = filter_google_songs(
			playlist_songs, include_filters=include_filters, exclude_filters=exclude_filters,
			all_includes=all_includes, all_excludes=all_excludes
		)

		logger.info("Filtered {0} Google playlist songs".format(len(filtered_songs)))
		logger.info("Loaded {0} Google playlist songs".format(len(matched_songs)))

		return matched_songs, filtered_songs