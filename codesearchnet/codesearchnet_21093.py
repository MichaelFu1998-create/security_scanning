def objHasUnsavedChanges(self):
		'''
			objHasUnsavedChanges - @see ForeignLinkData.objHasUnsavedChanges

			True if ANY object has unsaved changes.
		'''
		if not self.obj:
			return False

		for thisObj in self.obj:
			if not thisObj:
				continue
			if thisObj.hasUnsavedChanges(cascadeObjects=True):
				return True

		return False