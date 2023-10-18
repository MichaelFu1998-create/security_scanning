def _get_new_connection(self):
		'''
			_get_new_connection - Get a new connection
			internal
		'''
		pool = getRedisPool(self.mdl.REDIS_CONNECTION_PARAMS)
		return redis.Redis(connection_pool=pool)