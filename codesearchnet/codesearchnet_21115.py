def save(self):
		'''
			save - Save all objects in this list
		'''
		if len(self) == 0:
			return []
		mdl = self.getModel()
		return mdl.saver.save(self)