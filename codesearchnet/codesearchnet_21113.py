def getModel(self):
		'''
			getModel - get the IndexedRedisModel associated with this list. If one was not provided in constructor,
			  it will be inferred from the first item in the list (if present)

			  @return <None/IndexedRedisModel> - None if none could be found, otherwise the IndexedRedisModel type of the items in this list.

			@raises ValueError if first item is not the expected type.
		'''
		if not self.mdl and len(self) > 0:
			mdl = self[0].__class__
			self.__validate_model(mdl)

			self.mdl = mdl

		return self.mdl