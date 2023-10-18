def count(self):
		'''
			count - gets the number of records matching the filter criteria

			Example:
				theCount = Model.objects.filter(field1='value').count()
		'''
		conn = self._get_connection()
		
		numFilters = len(self.filters)
		numNotFilters = len(self.notFilters)
		if numFilters + numNotFilters == 0:
			return conn.scard(self._get_ids_key())

		if numNotFilters == 0:
			if numFilters == 1:
				(filterFieldName, filterValue) = self.filters[0]
				return conn.scard(self._get_key_for_index(filterFieldName, filterValue))
			indexKeys = [self._get_key_for_index(filterFieldName, filterValue) for filterFieldName, filterValue in self.filters]

			return len(conn.sinter(indexKeys))

		notIndexKeys = [self._get_key_for_index(filterFieldName, filterValue) for filterFieldName, filterValue in self.notFilters]
		if numFilters == 0:
			return len(conn.sdiff(self._get_ids_key(), *notIndexKeys))

		indexKeys = [self._get_key_for_index(filterFieldName, filterValue) for filterFieldName, filterValue in self.filters]
		
		tempKey = self._getTempKey()
		pipeline = conn.pipeline()
		pipeline.sinterstore(tempKey, *indexKeys)
		pipeline.sdiff(tempKey, *notIndexKeys)
		pipeline.delete(tempKey)
		pks = pipeline.execute()[1] # sdiff

		return len(pks)