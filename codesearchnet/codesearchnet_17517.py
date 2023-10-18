def download(self, songs, template=None):
		"""Download Google Music songs.

		Parameters:
			songs (list or dict): Google Music song dict(s).

			template (str): A filepath which can include template patterns.

		Returns:
			A list of result dictionaries.
			::

				[
					{'result': 'downloaded', 'id': song_id, 'filepath': downloaded[song_id]},  # downloaded
					{'result': 'error', 'id': song_id, 'message': error[song_id]}   # error
				]
		"""

		if not template:
			template = os.getcwd()

		songnum = 0
		total = len(songs)
		results = []
		errors = {}
		pad = len(str(total))

		for result in self._download(songs, template):
			song_id = songs[songnum]['id']
			songnum += 1

			downloaded, error = result

			if downloaded:
				logger.info(
					"({num:>{pad}}/{total}) Successfully downloaded -- {file} ({song_id})".format(
						num=songnum, pad=pad, total=total, file=downloaded[song_id], song_id=song_id
					)
				)

				results.append({'result': 'downloaded', 'id': song_id, 'filepath': downloaded[song_id]})
			elif error:
				title = songs[songnum].get('title', "<empty>")
				artist = songs[songnum].get('artist', "<empty>")
				album = songs[songnum].get('album', "<empty>")

				logger.info(
					"({num:>{pad}}/{total}) Error on download -- {title} -- {artist} -- {album} ({song_id})".format(
						num=songnum, pad=pad, total=total, title=title, artist=artist, album=album, song_id=song_id
					)
				)

				results.append({'result': 'error', 'id': song_id, 'message': error[song_id]})

		if errors:
			logger.info("\n\nThe following errors occurred:\n")
			for filepath, e in errors.items():
				logger.info("{file} | {error}".format(file=filepath, error=e))
			logger.info("\nThese files may need to be synced again.\n")

		return results