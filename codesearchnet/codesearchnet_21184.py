def first(self, cascadeFetch=False):
		'''
			First - Returns the oldest record (lowerst primary key) with current filters.
				This makes an efficient queue, as it only fetches a single object.
		

			@param cascadeFetch <bool> Default False, If True, all Foreign objects associated with this model
			   will be fetched immediately. If False, foreign objects will be fetched on-access.

			@return - Instance of Model object, or None if no items match current filters
		'''
		obj = None

		matchedKeys = self.getPrimaryKeys(sortByAge=True)
		if matchedKeys:
			# Loop so we don't return None when there are items, if item is deleted between getting key and getting obj
			while matchedKeys and obj is None:
				obj = self.get(matchedKeys.pop(0), cascadeFetch=cascadeFetch)

		return obj