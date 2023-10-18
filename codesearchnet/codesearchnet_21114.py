def delete(self):
		'''
			delete - Delete all objects in this list.

			@return <int> - Number of objects deleted
		'''
		if len(self) == 0:
			return 0
		mdl = self.getModel()
		return mdl.deleter.deleteMultiple(self)