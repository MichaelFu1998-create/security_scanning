def refetch(self):
		'''
			refetch - Fetch a fresh copy of all items in this list.
				Returns a new list. To update in-place, use "reload".

			@return IRQueryableList<IndexedRedisModel> - List of fetched items
		'''

		if len(self) == 0:
			return IRQueryableList()

		mdl = self.getModel()
		pks = [item._id for item in self if item._id]

		return mdl.objects.getMultiple(pks)