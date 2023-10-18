def is_hidden(path):
	"""
	Check whether a file is presumed hidden, either because
	the pathname starts with dot or because the platform
	indicates such.
	"""
	full_path = os.path.abspath(path)
	name = os.path.basename(full_path)

	def no(path):
		return False
	platform_hidden = globals().get('is_hidden_' + platform.system(), no)
	return name.startswith('.') or platform_hidden(full_path)