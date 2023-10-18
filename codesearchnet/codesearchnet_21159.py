def saveToExternal(self, redisCon):
		'''
			saveToExternal - Saves this object to a different Redis than that specified by REDIS_CONNECTION_PARAMS on this model.

			@param redisCon <dict/redis.Redis> - Either a dict of connection params, a la REDIS_CONNECTION_PARAMS, or an existing Redis connection.
				If you are doing a lot of bulk copies, it is recommended that you create a Redis connection and pass it in rather than establish a new
				connection with each call.

			@note - You will generate a new primary key relative to the external Redis environment. If you need to reference a "shared" primary key, it is better
					to use an indexed field than the internal pk.

		'''
		if type(redisCon) == dict:
			conn = redis.Redis(**redisCon)
		elif hasattr(conn, '__class__') and issubclass(conn.__class__, redis.Redis):
			conn = redisCon
		else:
			raise ValueError('saveToExternal "redisCon" param must either be a dictionary of connection parameters, or redis.Redis, or extension thereof')

		saver = self.saver

		# Fetch next PK from external
		forceID = saver._getNextID(conn) # Redundant because of changes in save method
		myCopy = self.copy(False)

		return saver.save(myCopy, usePipeline=True, forceID=forceID, conn=conn)