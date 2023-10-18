def compat_convertHashedIndexes(self, objs, conn=None):
		'''
			compat_convertHashedIndexes - Reindex all fields for the provided objects, where the field value is hashed or not.
			If the field is unhashable, do not allow.

			NOTE: This works one object at a time. It is intended to be used while your application is offline,
			  as it doesn't make sense to be changing your model while applications are actively using it.

			@param objs <IndexedRedisModel objects to convert>
			@param conn <redis.Redis or None> - Specific Redis connection or None to reuse.
		'''
		if conn is None:
			conn = self._get_connection()



		# Do one pipeline per object.
		#  XXX: Maybe we should do the whole thing in one pipeline? 

		fields = []        # A list of the indexed fields

		# Iterate now so we do this once instead of per-object.
		for indexedField in self.indexedFields:

			origField = self.fields[indexedField]

			# Check if type supports configurable hashIndex, and if not skip it.
			if 'hashIndex' not in origField.__class__.__new__.__code__.co_varnames:
				continue

			if indexedField.hashIndex is True:
				hashingField = origField

				regField = origField.copy()
				regField.hashIndex = False
			else:
				regField = origField
				# Maybe copy should allow a dict of override params?
				hashingField = origField.copy()
				hashingField.hashIndex = True


			fields.append ( (origField, regField, hashingField) )

		objDicts = [obj.asDict(True, forStorage=True) for obj in objs]

		# Iterate over all values. Remove the possibly stringed index, the possibly hashed index, and then put forth the hashed index.

		for objDict in objDicts:
			pipeline = conn.pipeline()
			pk = objDict['_id']
			for origField, regField, hashingField in fields:
				val = objDict[indexedField]

				# Remove the possibly stringed index
				self._rem_id_from_index(regField, pk, val, pipeline)
				# Remove the possibly hashed index
				self._rem_id_from_index(hashingField, pk, val, pipeline)
				# Add the new (hashed or unhashed) form.
				self._add_id_to_index(origField, pk, val, pipeline)

			# Launch all at once
			pipeline.execute()