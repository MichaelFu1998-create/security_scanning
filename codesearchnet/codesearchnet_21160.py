def reload(self, cascadeObjects=True):
		'''
                reload - Reload this object from the database, overriding any local changes and merging in any updates.


		    @param cascadeObjects <bool> Default True. If True, foreign-linked objects will be reloaded if their values have changed
		      since last save/fetch. If False, only if the pk changed will the foreign linked objects be reloaded.

                    @raises KeyError - if this object has not been saved (no primary key)

                    @return - Dict with the keys that were updated. Key is field name that was updated,
		       and value is tuple of (old value, new value). 

		    NOTE: Currently, this will cause a fetch of all Foreign Link objects, one level

		'''
		_id = self._id
		if not _id:
			raise KeyError('Object has never been saved! Cannot reload.')

		currentData = self.asDict(False, forStorage=False)

		# Get the object, and compare the unconverted "asDict" repr.
		#  If any changes, we will apply the already-convered value from
		#  the object, but we compare the unconverted values (what's in the DB).
		newDataObj = self.objects.get(_id)
		if not newDataObj:
			raise KeyError('Object with id=%d is not in database. Cannot reload.' %(_id,))

		newData = newDataObj.asDict(False, forStorage=False)
		if currentData == newData and not self.foreignFields:
			return []

		updatedFields = {}
		for thisField, newValue in newData.items():
			defaultValue = thisField.getDefaultValue()

			currentValue = currentData.get(thisField, defaultValue)

			fieldIsUpdated = False

			if currentValue != newValue:
				fieldIsUpdated = True
			elif cascadeObjects is True and issubclass(thisField.__class__, IRForeignLinkFieldBase):
				# If we are cascading objects, and at this point the pk is the same

				if currentValue.isFetched():
					# If we have fetched the current set, we might need to update (pks already match)
					oldObjs = currentValue.getObjs()
					newObjs = newValue.getObjs()

					if oldObjs != newObjs: # This will check using __eq__, so one-level including pk
						fieldIsUpdated = True
					else:
						# Use hasSameValues with cascadeObjects=True to scan past one level
						for i in range(len(oldObjs)):
							if not oldObjs[i].hasSameValues(newObjs[i], cascadeObjects=True):
								fieldIsUpdated = True
								break

			if fieldIsUpdated is True:
				# Use "converted" values in the updatedFields dict, and apply on the object.
				updatedFields[thisField] = ( currentValue, newValue) 
				setattr(self, thisField, newValue)
				self._origData[thisField] = newDataObj._origData[thisField]


		return updatedFields