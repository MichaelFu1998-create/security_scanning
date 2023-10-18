def _toStorage(self, value):
		'''
			_toStorage - Convert the value to a string representation for storage.

			@param value - The value of the item to convert
			@return A string value suitable for storing.
		'''

		for chainedField in self.chainedFields:
			value = chainedField.toStorage(value)

		return value