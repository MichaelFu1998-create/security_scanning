def getPrimaryKeys(self, sortByAge=False):
		'''
			getPrimaryKeys - Returns all primary keys matching current filterset.

			@param sortByAge <bool> - If False, return will be a set and may not be ordered.
				If True, return will be a list and is guarenteed to represent objects oldest->newest

			@return <set> - A set of all primary keys associated with current filters.
		'''
		conn = self._get_connection()
		# Apply filters, and return object
		numFilters = len(self.filters)
		numNotFilters = len(self.notFilters)

		if numFilters + numNotFilters == 0:
			# No filters, get all.
			conn = self._get_connection()
			matchedKeys = conn.smembers(self._get_ids_key())

		elif numNotFilters == 0:
			# Only Inclusive
			if numFilters == 1:
				# Only one filter, get members of that index key
				(filterFieldName, filterValue) = self.filters[0]
				matchedKeys = conn.smembers(self._get_key_for_index(filterFieldName, filterValue))
			else:
				# Several filters, intersect the index keys
				indexKeys = [self._get_key_for_index(filterFieldName, filterValue) for filterFieldName, filterValue in self.filters]
				matchedKeys = conn.sinter(indexKeys)

		else:
			# Some negative filters present
			notIndexKeys = [self._get_key_for_index(filterFieldName, filterValue) for filterFieldName, filterValue in self.notFilters]
			if numFilters == 0:
				# Only negative, diff against all keys
				matchedKeys = conn.sdiff(self._get_ids_key(), *notIndexKeys)
			else:
				# Negative and positive. Use pipeline, find all positive intersections, and remove negative matches
				indexKeys = [self._get_key_for_index(filterFieldName, filterValue) for filterFieldName, filterValue in self.filters]
				
				tempKey = self._getTempKey()
				pipeline = conn.pipeline()
				pipeline.sinterstore(tempKey, *indexKeys)
				pipeline.sdiff(tempKey, *notIndexKeys)
				pipeline.delete(tempKey)
				matchedKeys = pipeline.execute()[1] # sdiff


		matchedKeys = [ int(_key) for _key in matchedKeys ]

		if sortByAge is False:
			return list(matchedKeys)
		else:
			matchedKeys = list(matchedKeys)
			matchedKeys.sort()

			return matchedKeys