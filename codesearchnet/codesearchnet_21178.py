def exists(self, pk):
		'''
			exists - Tests whether a record holding the given primary key exists.

			@param pk - Primary key (see getPk method)

			Example usage: Waiting for an object to be deleted without fetching the object or running a filter. 

			This is a very cheap operation.

			@return <bool> - True if object with given pk exists, otherwise False
		'''
		conn = self._get_connection()
		key = self._get_key_for_id(pk)
		return conn.exists(key)