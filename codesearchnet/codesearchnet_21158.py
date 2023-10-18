def copy(self, copyPrimaryKey=False, copyValues=False):
		'''
                    copy - Copies this object.

                    @param copyPrimaryKey <bool> default False - If True, any changes to the copy will save over-top the existing entry in Redis.
                        If False, only the data is copied, and nothing is saved.

		    @param copyValues <bool> default False - If True, every field value on this object will be explicitly copied. If False,
		      an object will be created with the same values, and depending on the type may share the same reference.
		      
		      This is the difference between a copy and a deepcopy.

	            @return <IndexedRedisModel> - Copy of this object, per above

		    If you need a copy that IS linked, @see IndexedRedisModel.copy
		'''
		cpy = self.__class__(**self.asDict(copyPrimaryKey, forStorage=False))
		if copyValues is True:
			for fieldName in cpy.FIELDS:
				setattr(cpy, fieldName, copy.deepcopy(getattr(cpy, fieldName)))
		return cpy