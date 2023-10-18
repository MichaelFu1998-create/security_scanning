def asDict(self, includeMeta=False, forStorage=False, strKeys=False):
		'''
			toDict / asDict - Get a dictionary representation of this model.

			@param includeMeta - Include metadata in return. For now, this is only pk stored as "_id"

			@param convertValueTypes <bool> - default True. If False, fields with fieldValue defined will be converted to that type.
				Use True when saving, etc, as native type is always either str or bytes.

			@param strKeys <bool> Default False - If True, just the string value of the field name will be used as the key.
				Otherwise, the IRField itself will be (although represented and indexed by string)

			@return - Dictionary reprensetation of this object and all fields
		'''
		ret = {}
		for thisField in self.FIELDS:
			val = object.__getattribute__(self, thisField)

			if forStorage is True:
				val = thisField.toStorage(val)

			if strKeys:
				ret[str(thisField)] = val
			else:
				ret[thisField] = val


		if includeMeta is True:
			ret['_id'] = getattr(self, '_id', None)
		return ret