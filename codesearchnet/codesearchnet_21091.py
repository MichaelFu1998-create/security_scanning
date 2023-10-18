def getObj(self):
		'''
			getObj - @see ForeignLinkData.getObj

				Except this always returns a list
		'''
		if self.obj:
			needPks = [ (i, self.pk[i]) for i in range(len(self.obj)) if self.obj[i] is None]

			if not needPks:
				return self.obj

			fetched = list(self.foreignModel.objects.getMultiple([needPk[1] for needPk in needPks]))
			
			i = 0
			for objIdx, pk in needPks:
				self.obj[objIdx] = fetched[i]
				i += 1

		return self.obj