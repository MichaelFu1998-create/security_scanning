def _rem_id_from_keys(self, pk, conn=None):
		'''
			_rem_id_from_keys - Remove primary key from table
			internal
		'''
		if conn is None:
			conn = self._get_connection()
		conn.srem(self._get_ids_key(), pk)