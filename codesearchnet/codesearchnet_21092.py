def isFetched(self):
		'''
			isFetched - @see ForeignLinkData.isFetched
		'''
		if not self.obj:
			return False

		if not self.pk or None in self.obj:
			return False
		return not bool(self.obj is None)