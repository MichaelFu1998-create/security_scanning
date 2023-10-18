def compat_convertHashedIndexes(self, fetchAll=True):
		'''
			compat_convertHashedIndexes - Reindex fields, used for when you change the propery "hashIndex" on one or more fields.

			For each field, this will delete both the hash and unhashed keys to an object, 
			  and then save a hashed or unhashed value, depending on that field's value for "hashIndex".

			For an IndexedRedisModel class named "MyModel", call as "MyModel.objects.compat_convertHashedIndexes()"

			NOTE: This works one object at a time (regardless of #fetchAll), so that an unhashable object does not trash all data.

			This method is intended to be used while your application is offline,
			  as it doesn't make sense to be changing your model while applications are actively using it.

			@param fetchAll <bool>, Default True - If True, all objects will be fetched first, then converted.
			  This is generally what you want to do, as it is more efficient. If you are memory contrainted,
			  you can set this to "False", and it will fetch one object at a time, convert it, and save it back.

		'''

		saver = IndexedRedisSave(self.mdl)

		if fetchAll is True:
			objs = self.all()
			saver.compat_convertHashedIndexes(objs)
		else:
			didWarnOnce = False

			pks = self.getPrimaryKeys()
			for pk in pks:
				obj = self.get(pk)
				if not obj:
					if didWarnOnce is False:
						sys.stderr.write('WARNING(once)! An object (type=%s , pk=%d) disappered while '  \
							'running compat_convertHashedIndexes! This probably means an application '  \
							'is using the model while converting indexes. This is a very BAD IDEA (tm).')
						
						didWarnOnce = True
					continue
				saver.compat_convertHashedIndexes([obj])