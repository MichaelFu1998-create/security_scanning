def get_supported_filepaths(filepaths, supported_extensions, max_depth=float('inf')):
	"""Get filepaths with supported extensions from given filepaths.

	Parameters:
		filepaths (list or str): Filepath(s) to check.

		supported_extensions (tuple or str): Supported file extensions or a single file extension.

		max_depth (int): The depth in the directory tree to walk.
			A depth of '0' limits the walk to the top directory.
			Default: No limit.

	Returns:
		A list of supported filepaths.
	"""

	supported_filepaths = []

	for path in filepaths:
		if os.name == 'nt' and CYGPATH_RE.match(path):
			path = convert_cygwin_path(path)

		if os.path.isdir(path):
			for root, __, files in walk_depth(path, max_depth):
				for f in files:
					if f.lower().endswith(supported_extensions):
						supported_filepaths.append(os.path.join(root, f))
		elif os.path.isfile(path) and path.lower().endswith(supported_extensions):
			supported_filepaths.append(path)

	return supported_filepaths