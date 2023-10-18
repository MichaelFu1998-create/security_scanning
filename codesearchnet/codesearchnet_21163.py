def connectAlt(cls, redisConnectionParams):
		'''
			connectAlt - Create a class of this model which will use an alternate connection than the one specified by REDIS_CONNECTION_PARAMS on this model.

			@param redisConnectionParams <dict> - Dictionary of arguments to redis.Redis, same as REDIS_CONNECTION_PARAMS.

			@return - A class that can be used in all the same ways as the existing IndexedRedisModel, but that connects to a different instance.

			  The fields and key will be the same here, but the connection will be different. use #copyModel if you want an independent class for the model
		'''
		if not isinstance(redisConnectionParams, dict):
			raise ValueError('redisConnectionParams must be a dictionary!')

		hashVal = hashDictOneLevel(redisConnectionParams)

		modelDictCopy = copy.deepcopy(dict(cls.__dict__))
		modelDictCopy['REDIS_CONNECTION_PARAMS'] = redisConnectionParams

		ConnectedIndexedRedisModel = type('AltConnect' + cls.__name__ + str(hashVal), cls.__bases__, modelDictCopy)

		return ConnectedIndexedRedisModel