def getPk(self):
		'''
			getPk - @see ForeignLinkData.getPk
		'''
		if not self.pk or None in self.pk:
			for i in range( len(self.pk) ):
				if self.pk[i]:
					continue

				if self.obj[i] and self.obj[i]._id:
					self.pk[i] = self.obj[i]._id

		return self.pk