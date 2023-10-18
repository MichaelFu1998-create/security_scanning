def allByAge(self, cascadeFetch=False):
		'''
			allByAge - Get the underlying objects which match the filter criteria, ordered oldest -> newest
				If you are doing a queue or just need the head/tail, consider .first() and .last() instead.


			@param cascadeFetch <bool> Default False, If True, all Foreign objects associated with this model
			   will be fetched immediately. If False, foreign objects will be fetched on-access.

			@return - Objects of the Model instance associated with this query, sorted oldest->newest
		'''
		matchedKeys = self.getPrimaryKeys(sortByAge=True)
		if matchedKeys:
			return self.getMultiple(matchedKeys, cascadeFetch=cascadeFetch)

		return IRQueryableList([], mdl=self.mdl)