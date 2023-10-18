def deleteMultipleByPks(self, pks):
		'''
			deleteMultipleByPks - Delete multiple objects given their primary keys

			@param pks - List of primary keys

			@return - Number of objects deleted
		'''
		if type(pks) == set:
			pks = list(pks)

		if len(pks) == 1:
			return self.deleteByPk(pks[0])

		objs = self.mdl.objects.getMultipleOnlyIndexedFields(pks)
		return self.deleteMultiple(objs)