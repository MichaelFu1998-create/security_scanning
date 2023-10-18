def reindex(self, objs, conn=None):
		'''
			reindex - Reindexes a given list of objects. Probably you want to do Model.objects.reindex() instead of this directly.

			@param objs list<IndexedRedisModel> - List of objects to reindex
			@param conn <redis.Redis or None> - Specific Redis connection or None to reuse
		'''
		if conn is None:
			conn = self._get_connection()

		pipeline = conn.pipeline()

		objDicts = [obj.asDict(True, forStorage=True) for obj in objs]

		for indexedFieldName in self.indexedFields:
			for objDict in objDicts:
				self._rem_id_from_index(indexedFieldName, objDict['_id'], objDict[indexedFieldName], pipeline)
				self._add_id_to_index(indexedFieldName, objDict['_id'], objDict[indexedFieldName], pipeline)

		pipeline.execute()