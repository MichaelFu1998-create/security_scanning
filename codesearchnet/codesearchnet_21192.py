def reindex(self):
		'''
			reindex - Reindexes the objects matching current filterset. Use this if you add/remove a field to INDEXED_FIELDS.

			  NOTE - This will NOT remove entries from the old index if you change index type, or change decimalPlaces on a
			    IRFixedPointField.  To correct these indexes, you'll need to run:

			       Model.reset(Model.objects.all())

			If you change the value of "hashIndex" on a field, you need to call #compat_convertHashedIndexes instead.
		'''
		objs = self.all()
		saver = IndexedRedisSave(self.mdl)
		saver.reindex(objs)