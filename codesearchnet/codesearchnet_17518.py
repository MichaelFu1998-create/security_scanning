def upload(self, filepaths, enable_matching=False, transcode_quality='320k', delete_on_success=False):
		"""Upload local songs to Google Music.

		Parameters:
			filepaths (list or str): Filepath(s) to upload.

			enable_matching (bool): If ``True`` attempt to use `scan and match
				<http://support.google.com/googleplay/bin/answer.py?hl=en&answer=2920799&topic=2450455>`__.
				This requieres ffmpeg or avconv.

			transcode_quality (str or int): If int, pass to ffmpeg/avconv ``-q:a`` for libmp3lame `VBR quality
				<http://trac.ffmpeg.org/wiki/Encode/MP3#VBREncoding>'__.
				If string, pass to ffmpeg/avconv ``-b:a`` for libmp3lame `CBR quality
				<http://trac.ffmpeg.org/wiki/Encode/MP3#CBREncoding>'__.
				Default: ``320k``

			delete_on_success (bool): Delete successfully uploaded local files. Default: ``False``

		Returns:
			A list of result dictionaries.
			::

				[
					{'result': 'uploaded', 'filepath': <filepath>, 'id': <song_id>},  # uploaded
					{'result': 'matched', 'filepath': <filepath>, 'id': <song_id>},  # matched
					{'result': 'error', 'filepath': <filepath>, 'message': <error_message>},  # error
					{'result': 'not_uploaded', 'filepath': <filepath>, 'id': <song_id>, 'message': <reason_message>},  # not_uploaded ALREADY_EXISTS
					{'result': 'not_uploaded', 'filepath': <filepath>, 'message': <reason_message>}  # not_uploaded
				]
		"""

		filenum = 0
		total = len(filepaths)
		results = []
		errors = {}
		pad = len(str(total))
		exist_strings = ["ALREADY_EXISTS", "this song is already uploaded"]

		for result in self._upload(filepaths, enable_matching=enable_matching, transcode_quality=transcode_quality):
			filepath = filepaths[filenum]
			filenum += 1

			uploaded, matched, not_uploaded, error = result

			if uploaded:
				logger.info(
					"({num:>{pad}}/{total}) Successfully uploaded -- {file} ({song_id})".format(
						num=filenum, pad=pad, total=total, file=filepath, song_id=uploaded[filepath]
					)
				)

				results.append({'result': 'uploaded', 'filepath': filepath, 'id': uploaded[filepath]})
			elif matched:
				logger.info(
					"({num:>{pad}}/{total}) Successfully scanned and matched -- {file} ({song_id})".format(
						num=filenum, pad=pad, total=total, file=filepath, song_id=matched[filepath]
					)
				)

				results.append({'result': 'matched', 'filepath': filepath, 'id': matched[filepath]})
			elif error:
				logger.warning("({num:>{pad}}/{total}) Error on upload -- {file}".format(num=filenum, pad=pad, total=total, file=filepath))

				results.append({'result': 'error', 'filepath': filepath, 'message': error[filepath]})
				errors.update(error)
			else:
				if any(exist_string in not_uploaded[filepath] for exist_string in exist_strings):
					response = "ALREADY EXISTS"

					song_id = GM_ID_RE.search(not_uploaded[filepath]).group(0)

					logger.info(
						"({num:>{pad}}/{total}) Failed to upload -- {file} ({song_id}) | {response}".format(
							num=filenum, pad=pad, total=total, file=filepath, response=response, song_id=song_id
						)
					)

					results.append({'result': 'not_uploaded', 'filepath': filepath, 'id': song_id, 'message': not_uploaded[filepath]})
				else:
					response = not_uploaded[filepath]

					logger.info(
						"({num:>{pad}}/{total}) Failed to upload -- {file} | {response}".format(
							num=filenum, pad=pad, total=total, file=filepath, response=response
						)
					)

					results.append({'result': 'not_uploaded', 'filepath': filepath, 'message': not_uploaded[filepath]})

			success = (uploaded or matched) or (not_uploaded and 'ALREADY_EXISTS' in not_uploaded[filepath])

			if success and delete_on_success:
				try:
					os.remove(filepath)
				except (OSError, PermissionError):
					logger.warning("Failed to remove {} after successful upload".format(filepath))

		if errors:
			logger.info("\n\nThe following errors occurred:\n")

			for filepath, e in errors.items():
				logger.info("{file} | {error}".format(file=filepath, error=e))
			logger.info("\nThese filepaths may need to be synced again.\n")

		return results