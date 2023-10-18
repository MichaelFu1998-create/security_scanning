def walk_depth(path, max_depth=float('inf')):
	"""Walk a directory tree with configurable depth.

	Parameters:
		path (str): A directory path to walk.

		max_depth (int): The depth in the directory tree to walk.
			A depth of '0' limits the walk to the top directory.
			Default: No limit.
	"""

	start_level = os.path.abspath(path).count(os.path.sep)

	for dir_entry in os.walk(path):
		root, dirs, _ = dir_entry
		level = root.count(os.path.sep) - start_level

		yield dir_entry

		if level >= max_depth:
			dirs[:] = []