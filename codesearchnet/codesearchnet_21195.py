def _doSave(self, obj, isInsert, conn, pipeline=None):
		'''
			_doSave - Internal function to save a single object. Don't call this directly. 
			            Use "save" instead.

			  If a pipeline is provided, the operations (setting values, updating indexes, etc)
			    will be queued into that pipeline.
			  Otherwise, everything will be executed right away.

			  @param obj - Object to save
			  @param isInsert - Bool, if insert or update. Either way, obj._id is expected to be set.
			  @param conn - Redis connection
			  @param pipeline - Optional pipeline, if present the items will be queued onto it. Otherwise, go directly to conn.
		'''

		if pipeline is None:
			pipeline = conn

		newDict = obj.asDict(forStorage=True)
		key = self._get_key_for_id(obj._id)

		if isInsert is True:
			for thisField in self.fields:

				fieldValue = newDict.get(thisField, thisField.getDefaultValue())

				pipeline.hset(key, thisField, fieldValue)

				# Update origData with the new data
				if fieldValue == IR_NULL_STR:
					obj._origData[thisField] = irNull
				else:
					obj._origData[thisField] = object.__getattribute__(obj, str(thisField))

			self._add_id_to_keys(obj._id, pipeline)

			for indexedField in self.indexedFields:
				self._add_id_to_index(indexedField, obj._id, obj._origData[indexedField], pipeline)
		else:
			updatedFields = obj.getUpdatedFields()
			for thisField, fieldValue in updatedFields.items():
				(oldValue, newValue) = fieldValue

				oldValueForStorage = thisField.toStorage(oldValue)
				newValueForStorage = thisField.toStorage(newValue)

				pipeline.hset(key, thisField, newValueForStorage)

				if thisField in self.indexedFields:
					self._rem_id_from_index(thisField, obj._id, oldValueForStorage, pipeline)
					self._add_id_to_index(thisField, obj._id, newValueForStorage, pipeline)

				# Update origData with the new data
				obj._origData[thisField] = newValue