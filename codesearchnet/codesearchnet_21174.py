def _getNextID(self, conn=None):
		'''
			_getNextID - Get (and increment) the next primary key for this model.
				If you don't want to increment, @see _peekNextID .
				Internal.
				This is done automatically on save. No need to call it.

			@return int - next pk
		'''
		if conn is None:
			conn = self._get_connection()
		return int(conn.incr(self._get_next_id_key()))