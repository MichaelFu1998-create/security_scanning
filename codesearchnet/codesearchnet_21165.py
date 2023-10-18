def _get_connection(self):
		'''
			_get_connection - Maybe get a new connection, or reuse if passed in.
				Will share a connection with a model
			internal
		'''
		if self._connection is None:
			self._connection = self._get_new_connection() 
		return self._connection