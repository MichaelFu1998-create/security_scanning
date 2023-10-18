def getUpdatedFields(self, cascadeObjects=False):
		'''
			getUpdatedFields - See changed fields.
			
			@param cascadeObjects <bool> default False, if True will check if any foreign linked objects themselves have unsaved changes (recursively).
				Otherwise, will just check if the pk has changed.

			@return - a dictionary of fieldName : tuple(old, new).

			fieldName may be a string or may implement IRField (which implements string, and can be used just like a string)
		'''
		updatedFields = {}
		for thisField in self.FIELDS:
			thisVal = object.__getattribute__(self, thisField)
			if self._origData.get(thisField, '') != thisVal:
				updatedFields[thisField] = (self._origData[thisField], thisVal)

			if cascadeObjects is True and issubclass(thisField.__class__, IRForeignLinkFieldBase) and thisVal.objHasUnsavedChanges():
				updatedFields[thisField] = (self._origData[thisField], thisVal)
					
		return updatedFields