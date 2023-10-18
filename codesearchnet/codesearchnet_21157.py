def hasSameValues(self, other, cascadeObject=True):
		'''
			hasSameValues - Check if this and another model have the same fields and values.

			This does NOT include id, so the models can have the same values but be different objects in the database.

			@param other <IndexedRedisModel> - Another model

			@param cascadeObject <bool> default True - If True, foreign link values with changes will be considered a difference.
				Otherwise, only the immediate values are checked.

			@return <bool> - True if all fields have the same value, otherwise False
		'''
		if self.FIELDS != other.FIELDS:
			return False

		oga = object.__getattribute__

		for field in self.FIELDS:
			thisVal = oga(self, field)
			otherVal = oga(other, field)
			if thisVal != otherVal:
				return False

			if cascadeObject is True and issubclass(field.__class__, IRForeignLinkFieldBase):
				if thisVal and thisVal.isFetched():
					if otherVal and otherVal.isFetched():
						theseForeign = thisVal.getObjs()
						othersForeign = otherVal.getObjs()
						 
						for i in range(len(theseForeign)):
							if not theseForeign[i].hasSameValues(othersForeign[i]):
								return False
					else:
						theseForeign = thisVal.getObjs()

						for i in range(len(theseForeign)):
							if theseForeign[i].hasUnsavedChanges(cascadeObjects=True):
								return False
				else:
					if otherVal and otherVal.isFetched():
						othersForeign = otherVal.getObjs()

						for i in range(len(othersForeign)):
							if othersForeign[i].hasUnsavedChanges(cascadeObjects=True):
								return False

							
				

		return True