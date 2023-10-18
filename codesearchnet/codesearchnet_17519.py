def convert_cygwin_path(path):
	"""Convert Unix path from Cygwin to Windows path."""

	try:
		win_path = subprocess.check_output(["cygpath", "-aw", path], universal_newlines=True).strip()
	except (FileNotFoundError, subprocess.CalledProcessError):
		logger.exception("Call to cygpath failed.")
		raise

	return win_path