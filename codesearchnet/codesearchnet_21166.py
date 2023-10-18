def _add_id_to_keys(self, pk, conn=None):
		'''
			_add_id_to_keys - Adds primary key to table
			internal
		'''
		if conn is None:
			conn = self._get_connection()
		conn.sadd(self._get_ids_key(), pk)