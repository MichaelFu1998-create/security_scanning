def deleteOne(self, obj, conn=None):
		'''
			deleteOne - Delete one object

			@param obj - object to delete
			@param conn - Connection to reuse, or None

			@return - number of items deleted (0 or 1)
		'''
		if not getattr(obj, '_id', None):
			return 0

		if conn is None:
			conn = self._get_connection()
			pipeline = conn.pipeline()
			executeAfter = True
		else:
			pipeline = conn # In this case, we are inheriting a pipeline
			executeAfter = False
		
		pipeline.delete(self._get_key_for_id(obj._id))
		self._rem_id_from_keys(obj._id, pipeline)
		for indexedFieldName in self.indexedFields:
			self._rem_id_from_index(indexedFieldName, obj._id, obj._origData[indexedFieldName], pipeline)

		obj._id = None

		if executeAfter is True:
			pipeline.execute()

		return 1