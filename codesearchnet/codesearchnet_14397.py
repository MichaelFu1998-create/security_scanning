def _debug(message, color=None, attrs=None):
		"""
		Print a message if the class attribute 'verbose' is enabled

		Args:
			message (str): Message to print
		"""
		if attrs is None:
			attrs = []
		if color is not None:
			print colored(message, color, attrs=attrs)
		else:
			if len(attrs) > 0:
				print colored(message, "white", attrs=attrs)
			else:
				print message