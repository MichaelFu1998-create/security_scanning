def compare_song_collections(src_songs, dst_songs):
	"""Compare two song collections to find missing songs.

	Parameters:
		src_songs (list): Google Music song dicts or filepaths of local songs.

		dest_songs (list): Google Music song dicts or filepaths of local songs.

	Returns:
		A list of Google Music song dicts or local song filepaths from source missing in destination.
	"""

	def gather_field_values(song):
		return tuple((_normalize_metadata(song[field]) for field in _filter_comparison_fields(song)))

	dst_songs_criteria = {gather_field_values(_normalize_song(dst_song)) for dst_song in dst_songs}

	return [src_song for src_song in src_songs if gather_field_values(_normalize_song(src_song)) not in dst_songs_criteria]