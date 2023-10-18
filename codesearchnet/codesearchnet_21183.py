def allOnlyIndexedFields(self):
		'''
			allOnlyIndexedFields - Get the objects which match the filter criteria, only fetching indexed fields.

			@return - Partial objects with only the indexed fields fetched
		'''
		matchedKeys = self.getPrimaryKeys()
		if matchedKeys:
			return self.getMultipleOnlyIndexedFields(matchedKeys)

		return IRQueryableList([], mdl=self.mdl)