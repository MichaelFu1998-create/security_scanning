def path(self, value):
		"""
		Setter for 'path' property

		Args:
			value (str): Absolute path to scan

		"""
		if not value.endswith('/'):
			self._path = '{v}/'.format(v=value)
		else:
			self._path = value