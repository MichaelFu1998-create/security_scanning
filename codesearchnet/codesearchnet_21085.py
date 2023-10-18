def _getReprProperties(self):
		'''
			_getReprProperties - Get the properties of this field to display in repr().

				These should be in the form of $propertyName=$propertyRepr

				The default IRField implementation handles just the "hashIndex" property.

				defaultValue is part of "__repr__" impl. You should just extend this method
				with your object's properties instead of rewriting repr.

		'''
		ret = []
		if getattr(self, 'valueType', None) is not None:
			ret.append('valueType=%s' %(self.valueType.__name__, ))
		if hasattr(self, 'hashIndex'):
			ret.append('hashIndex=%s' %(self.hashIndex, ))

		return ret