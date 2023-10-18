def clearRedisPools():
	'''
		clearRedisPools - Disconnect all managed connection pools, 
		   and clear the connectiobn_pool attribute on all stored managed connection pools.

		   A "managed" connection pool is one where REDIS_CONNECTION_PARAMS does not define the "connection_pool" attribute.
		   If you define your own pools, IndexedRedis will use them and leave them alone.

		  This method will be called automatically after calling setDefaultRedisConnectionParams.

		  Otherwise, you shouldn't have to call it.. Maybe as some sort of disaster-recovery call..
	'''
	global RedisPools
	global _redisManagedConnectionParams

	for pool in RedisPools.values():
		try:
			pool.disconnect()
		except:
			pass
	
	for paramsList in _redisManagedConnectionParams.values():
		for params in paramsList:
			if 'connection_pool' in params:
				del params['connection_pool']
	
	RedisPools.clear()
	_redisManagedConnectionParams.clear()