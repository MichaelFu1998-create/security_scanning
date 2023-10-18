def potential(self, value):
		"""
		Setter for 'potential' property

		Args:
			value (bool): True if a potential is required. False else

		"""
		if value:
			self._potential = True
		else:
			self._potential = False