def objHasUnsavedChanges(self):
		'''
			objHasUnsavedChanges - Check if any object has unsaved changes, cascading.
		'''
		if not self.obj:
			return False

		return self.obj.hasUnsavedChanges(cascadeObjects=True)