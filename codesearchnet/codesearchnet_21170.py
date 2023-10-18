def _get_key_for_index(self, indexedField, val):
		'''
			_get_key_for_index - Returns the key name that would hold the indexes on a value
			Internal - does not validate that indexedFields is actually indexed. Trusts you. Don't let it down.

			@param indexedField - string of field name
			@param val - Value of field

			@return - Key name string, potentially hashed.
		'''
		# If provided an IRField, use the toIndex from that (to support compat_ methods
		if hasattr(indexedField, 'toIndex'):
			val = indexedField.toIndex(val)
		else:
		# Otherwise, look up the indexed field from the model
			val = self.fields[indexedField].toIndex(val)


		return ''.join( [INDEXED_REDIS_PREFIX, self.keyName, ':idx:', indexedField, ':', val] )