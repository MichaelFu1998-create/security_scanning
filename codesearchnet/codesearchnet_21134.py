def _fromStorage(self, value):
		'''
			_fromStorage - Convert the value from storage (string) to the value type.

			@return - The converted value, or "irNull" if no value was defined (and field type is not default/string)
		'''

		for chainedField in reversed(self.chainedFields):
			value = chainedField._fromStorage(value)

		return value