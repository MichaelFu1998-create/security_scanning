def hasUnsavedChanges(self, cascadeObjects=False):
		'''
			hasUnsavedChanges - Check if any unsaved changes are present in this model, or if it has never been saved.

			@param cascadeObjects <bool> default False, if True will check if any foreign linked objects themselves have unsaved changes (recursively).
				Otherwise, will just check if the pk has changed.

			@return <bool> - True if any fields have changed since last fetch, or if never saved. Otherwise, False
		'''
		if not self._id or not self._origData:
			return True

		for thisField in self.FIELDS:
			thisVal = object.__getattribute__(self, thisField)
			if self._origData.get(thisField, '') != thisVal:
				return True

			if cascadeObjects is True and issubclass(thisField.__class__, IRForeignLinkFieldBase):
				if thisVal.objHasUnsavedChanges():
					return True

		return False