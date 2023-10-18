def all(self, cascadeFetch=False):
		'''
			all - Get the underlying objects which match the filter criteria.

			Example:   objs = Model.objects.filter(field1='value', field2='value2').all()

			@param cascadeFetch <bool> Default False, If True, all Foreign objects associated with this model
			   will be fetched immediately. If False, foreign objects will be fetched on-access.

			@return - Objects of the Model instance associated with this query.
		'''
		matchedKeys = self.getPrimaryKeys()
		if matchedKeys:
			return self.getMultiple(matchedKeys, cascadeFetch=cascadeFetch)

		return IRQueryableList([], mdl=self.mdl)