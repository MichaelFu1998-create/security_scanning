def _checkCanIndex(self):
		'''
			_checkCanIndex - Check if we CAN index (if all fields are indexable).
				Also checks the right-most field for "hashIndex" - if it needs to hash we will hash.
		'''

		# NOTE: We can't just check the right-most field. For types like pickle that don't support indexing, they don't
		#   support it because python2 and python3 have different results for pickle.dumps on the same object.
		#   So if we have a field chain like Pickle, Compressed   then we will have two different results.
		if not self.chainedFields:
			return (False, False)

		for chainedField in self.chainedFields:
			if chainedField.CAN_INDEX is False:
				return (False, False)

		return (True, self.chainedFields[-1].hashIndex)