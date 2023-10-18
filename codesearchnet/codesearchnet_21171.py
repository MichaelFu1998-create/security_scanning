def _compat_get_str_key_for_index(self, indexedField, val):
		'''
			_compat_get_str_key_for_index - Return the key name as a string, even if it is a hashed index field.
			  This is used in converting unhashed fields to a hashed index (called by _compat_rem_str_id_from_index which is called by compat_convertHashedIndexes)

			  @param inde
			@param indexedField - string of field name
			@param val - Value of field

			@return - Key name string, always a string regardless of hash
		'''
		return ''.join([INDEXED_REDIS_PREFIX, self.keyName, ':idx:', indexedField, ':', getattr(indexedField, 'toStorage', to_unicode)(val)])