def read_chunks(file, chunk_size=2048, update_func=lambda x: None):
	"""
	Read file in chunks of size chunk_size (or smaller).
	If update_func is specified, call it on every chunk with the amount
	read.
	"""
	while(True):
		res = file.read(chunk_size)
		if not res:
			break
		update_func(len(res))
		yield res