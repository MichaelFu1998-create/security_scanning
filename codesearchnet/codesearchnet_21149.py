def getRedisPool(params):
	'''
		getRedisPool - Returns and possibly also creates a Redis connection pool
			based on the REDIS_CONNECTION_PARAMS passed in.

			The goal of this method is to keep a small connection pool rolling
			to each unique Redis instance, otherwise during network issues etc
			python-redis will leak connections and in short-order can exhaust
			all the ports on a system. There's probably also some minor
			performance gain in sharing Pools.

			Will modify "params", if "host" and/or "port" are missing, will fill
			them in with defaults, and prior to return will set "connection_pool"
			on params, which will allow immediate return on the next call,
			and allow access to the pool directly from the model object.

			@param params <dict> - REDIS_CONNECTION_PARAMS - kwargs to redis.Redis

			@return redis.ConnectionPool corrosponding to this unique server.
	'''
	global RedisPools
	global _defaultRedisConnectionParams
	global _redisManagedConnectionParams

	if not params:
		params = _defaultRedisConnectionParams
		isDefaultParams = True
	else:
		isDefaultParams = bool(params is _defaultRedisConnectionParams)

	if 'connection_pool' in params:
		return params['connection_pool']

	hashValue = hashDictOneLevel(params)

	if hashValue in RedisPools:
		params['connection_pool'] = RedisPools[hashValue]
		return RedisPools[hashValue]
	
	# Copy the params, so that we don't modify the original dict
	if not isDefaultParams:
		origParams = params
		params = copy.copy(params)
	else:
		origParams = params

	checkAgain = False
	if 'host' not in params:
		if not isDefaultParams and 'host' in _defaultRedisConnectionParams:
			params['host'] = _defaultRedisConnectionParams['host']
		else:
			params['host'] = '127.0.0.1'
		checkAgain = True
	if 'port' not in params:
		if not isDefaultParams and 'port' in _defaultRedisConnectionParams:
			params['port'] = _defaultRedisConnectionParams['port']
		else:
			params['port'] = 6379
		checkAgain = True
	
	if 'db' not in params:
		if not isDefaultParams and 'db' in _defaultRedisConnectionParams:
			params['db'] = _defaultRedisConnectionParams['db']
		else:
			params['db'] = 0
		checkAgain = True


	if not isDefaultParams:
		otherGlobalKeys = set(_defaultRedisConnectionParams.keys()) - set(params.keys())
		for otherKey in otherGlobalKeys:
			if otherKey == 'connection_pool':
				continue
			params[otherKey] = _defaultRedisConnectionParams[otherKey]
			checkAgain = True

	if checkAgain:
		hashValue = hashDictOneLevel(params)
		if hashValue in RedisPools:
			params['connection_pool'] = RedisPools[hashValue]
			return RedisPools[hashValue]

	connectionPool = redis.ConnectionPool(**params)
	origParams['connection_pool'] = params['connection_pool'] = connectionPool
	RedisPools[hashValue] = connectionPool

	# Add the original as a "managed" redis connection (they did not provide their own pool)
	#   such that if the defaults change, we make sure to re-inherit any keys, and can disconnect
	#   from clearRedisPools
	origParamsHash = hashDictOneLevel(origParams)
	if origParamsHash not in _redisManagedConnectionParams:
		_redisManagedConnectionParams[origParamsHash] = [origParams]
	elif origParams not in _redisManagedConnectionParams[origParamsHash]:
		_redisManagedConnectionParams[origParamsHash].append(origParams)


	return connectionPool