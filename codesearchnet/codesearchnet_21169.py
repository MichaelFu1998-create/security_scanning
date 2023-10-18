def _rem_id_from_index(self, indexedField, pk, val, conn=None):
		'''
			_rem_id_from_index - Removes an id from an index
			internal
		'''
		if conn is None:
			conn = self._get_connection()
		conn.srem(self._get_key_for_index(indexedField, val), pk)