def allOnlyFields(self, fields, cascadeFetch=False):
		'''
			allOnlyFields - Get the objects which match the filter criteria, only fetching given fields.

			@param fields - List of fields to fetch

			@param cascadeFetch <bool> Default False, If True, all Foreign objects associated with this model
			   will be fetched immediately. If False, foreign objects will be fetched on-access.


			@return - Partial objects with only the given fields fetched
		'''
		matchedKeys = self.getPrimaryKeys()
		if matchedKeys:
			return self.getMultipleOnlyFields(matchedKeys, fields, cascadeFetch=cascadeFetch)

		return IRQueryableList([], mdl=self.mdl)