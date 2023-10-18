def reset(cls, newObjs):
		'''
			reset - Remove all stored data associated with this model (i.e. all objects of this type),
				and then save all the provided objects in #newObjs , all in one atomic transaction.

			Use this method to move from one complete set of objects to another, where any querying applications
			will only see the complete before or complete after.

			@param newObjs list<IndexedRedisModel objs> - A list of objects that will replace the current dataset

			To just replace a specific subset of objects in a single transaction, you can do MyModel.saver.save(objs)
			  and just the objs in "objs" will be inserted/updated in one atomic step.

			This method, on the other hand, will delete all previous objects and add the newly provided objects in a single atomic step,
			  and also reset the primary key ID generator

			@return list<int> - The new primary keys associated with each object (same order as provided #newObjs list)
		'''
		conn = cls.objects._get_new_connection()

		transaction = conn.pipeline()
		transaction.eval("""
		local matchingKeys = redis.call('KEYS', '%s*')

		for _,key in ipairs(matchingKeys) do
			redis.call('DEL', key)
		end
		""" %( ''.join([INDEXED_REDIS_PREFIX, cls.KEY_NAME, ':']), ), 0)
		saver = IndexedRedisSave(cls)
		nextID = 1
		for newObj in newObjs:
			saver.save(newObj, False, forceID=nextID, conn=transaction)
			nextID += 1
		transaction.set(saver._get_next_id_key(), nextID)
		transaction.execute()

		return list( range( 1, nextID, 1) )