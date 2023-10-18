def getPk(self):
		'''
			getPk - Resolve any absent pk's off the obj's (like if an obj has been saved), and return the pk.
		'''
		if not self.pk and self.obj:
			if self.obj._id:
				self.pk = self.obj._id

		return self.pk