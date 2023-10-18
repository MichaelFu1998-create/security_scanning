def copy(self):
		'''
			copy - Create a copy of this IRField.

			  Each subclass should implement this, as you'll need to pass in the args to constructor.

			@return <IRField (or subclass)> - Another IRField that has all the same values as this one.
		'''
		return self.__class__(name=self.name, valueType=self.valueType, defaultValue=self.defaultValue, hashIndex=self.hashIndex)