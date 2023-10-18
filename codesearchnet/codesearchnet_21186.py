def delete(self):
		'''
			delete - Deletes all entries matching the filter criteria

		'''
		if self.filters or self.notFilters:
			return self.mdl.deleter.deleteMultiple(self.allOnlyIndexedFields())
		return self.mdl.deleter.destroyModel()