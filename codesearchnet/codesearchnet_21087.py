def getObj(self):
		'''
			getObj - Fetch (if not fetched) and return the obj associated with this data.
		'''
		if self.obj is None:
			if not self.pk:
				return None
			self.obj = self.foreignModel.objects.get(self.pk)

		return self.obj