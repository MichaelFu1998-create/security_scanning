def deleteByPk(self, pk):
		'''
			deleteByPk - Delete object associated with given primary key
		'''
		obj = self.mdl.objects.getOnlyIndexedFields(pk)
		if not obj:
			return 0
		return self.deleteOne(obj)