def diff(firstObj, otherObj, includeMeta=False):
		'''
			diff - Compare the field values on two IndexedRedisModels.

			@param firstObj <IndexedRedisModel instance> - First object (or self)

			@param otherObj <IndexedRedisModel instance> - Second object

			@param includeMeta <bool> - If meta information (like pk) should be in the diff results.


			@return <dict> - Dict of  'field' : ( value_firstObjForField, value_otherObjForField ).
				
				Keys are names of fields with different values.
				Value is a tuple of ( value_firstObjForField, value_otherObjForField )

			Can be called statically, like: IndexedRedisModel.diff ( obj1, obj2 )

			  or in reference to an obj   : obj1.diff(obj2)
		'''

		if not isIndexedRedisModel(firstObj):	
			raise ValueError('Type < %s > does not extend IndexedRedisModel.' %( type(firstObj).__name__ , ) )
		if not isIndexedRedisModel(otherObj):	
			raise ValueError('Type < %s > does not extend IndexedRedisModel.' %( type(otherObj).__name__ , ) )

		firstObj.validateModel()
		otherObj.validateModel()

		# Types may not match, but could be subclass, special copy class (like connectAlt), etc.
		#   So check if FIELDS matches, and if so, we can continue.
		if getattr(firstObj, 'FIELDS') != getattr(otherObj, 'FIELDS'):
			# NOTE: Maybe we should iterate here and compare just that field types and names match?
			#   In case a copy changes a default or something, we would still be able to diff..
			raise ValueError('Cannot compare  < %s > and < %s > . Must be same model OR have equal FIELDS.' %( firstObj.__class__, otherObj.__class__) )
		
		diffFields = {}

		for thisField in firstObj.FIELDS:

			thisFieldStr = str(thisField)

			firstVal = object.__getattribute__( firstObj, thisFieldStr )
			otherVal = object.__getattribute__( otherObj, thisFieldStr )

			if firstVal != otherVal:
				diffFields[ thisFieldStr ] = ( (firstVal, otherVal) )

		if includeMeta:
			firstPk = firstObj.getPk()
			otherPk = otherObj.getPk()
			if firstPk != otherPk:
				diffFields['_id'] = ( firstPk, otherPk )

		return diffFields