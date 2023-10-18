def _peekNextID(self, conn=None):
		'''
			_peekNextID - Look at, but don't increment the primary key for this model.
				Internal.

			@return int - next pk
		'''
		if conn is None:
			conn = self._get_connection()
		return to_unicode(conn.get(self._get_next_id_key()) or 0)