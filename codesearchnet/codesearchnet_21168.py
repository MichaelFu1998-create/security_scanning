def _add_id_to_index(self, indexedField, pk, val, conn=None):
		'''
			_add_id_to_index - Adds an id to an index
			internal
		'''
		if conn is None:
			conn = self._get_connection()
		conn.sadd(self._get_key_for_index(indexedField, val), pk)