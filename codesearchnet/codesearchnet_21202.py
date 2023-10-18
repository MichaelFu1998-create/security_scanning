def destroyModel(self):
		'''
			destroyModel - Destroy everything related to this model in one swoop.

			    Same effect as Model.reset([]) - Except slightly more efficient.

			    This function is called if you do Model.objects.delete() with no filters set.

			@return - Number of keys deleted. Note, this is NOT number of models deleted, but total keys.
		'''
		conn = self._get_connection()
		pipeline = conn.pipeline()
		pipeline.eval("""
		local matchingKeys = redis.call('KEYS', '%s*')

		for _,key in ipairs(matchingKeys) do
			redis.call('DEL', key)
		end

		return #matchingKeys
		""" %( ''.join([INDEXED_REDIS_PREFIX, self.mdl.KEY_NAME, ':']), ), 0)
		return pipeline.execute()[0]