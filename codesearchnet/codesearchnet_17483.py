def get_google_playlist(self, playlist):
		"""Get playlist information of a user-generated Google Music playlist.

		Parameters:
			playlist (str): Name or ID of Google Music playlist. Names are case-sensitive.
				Google allows multiple playlists with the same name.
				If multiple playlists have the same name, the first one encountered is used.

		Returns:
			dict: The playlist dict as returned by Mobileclient.get_all_user_playlist_contents.
		"""

		logger.info("Loading playlist {0}".format(playlist))

		for google_playlist in self.api.get_all_user_playlist_contents():
			if google_playlist['name'] == playlist or google_playlist['id'] == playlist:
				return google_playlist
		else:
			logger.warning("Playlist {0} does not exist.".format(playlist))
			return {}