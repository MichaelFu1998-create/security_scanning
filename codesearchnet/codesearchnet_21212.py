def toBytes(self, value):
		'''
			toBytes - Convert a value to bytes using the encoding specified on this field

			@param value <str> - The field to convert to bytes

			@return <bytes> - The object encoded using the codec specified on this field.

			NOTE: This method may go away.
		'''
		if type(value) == bytes:
			return value
		return value.encode(self.getEncoding())