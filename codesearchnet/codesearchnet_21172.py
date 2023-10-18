def _compat_rem_str_id_from_index(self, indexedField, pk, val, conn=None):
		'''
			_compat_rem_str_id_from_index - Used in compat_convertHashedIndexes to remove the old string repr of a field,
				in order to later add the hashed value,
		'''
		if conn is None:
			conn = self._get_connection()
		conn.srem(self._compat_get_str_key_for_index(indexedField, val), pk)