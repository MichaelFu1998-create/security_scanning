def setDefaultRedisConnectionParams( connectionParams ):
	'''
		setDefaultRedisConnectionParams - Sets the default parameters used when connecting to Redis.

		  This should be the args to redis.Redis in dict (kwargs) form.

		  @param connectionParams <dict> - A dict of connection parameters.
		    Common keys are:

		       host <str> - hostname/ip of Redis server (default '127.0.0.1')
		       port <int> - Port number			(default 6379)
		       db  <int>  - Redis DB number		(default 0)

		   Omitting any of those keys will ensure the default value listed is used.

		  This connection info will be used by default for all connections to Redis, unless explicitly set otherwise.
		  The common way to override is to define REDIS_CONNECTION_PARAMS on a model, or use AltConnectedModel = MyModel.connectAlt( PARAMS )

		  Any omitted fields in these connection overrides will inherit the value from the global default.

		  For example, if your global default connection params define host = 'example.com', port=15000, and db=0, 
		    and then one of your models has
		       
		       REDIS_CONNECTION_PARAMS = { 'db' : 1 }
		    
		    as an attribute, then that model's connection will inherit host='example.com" and port=15000 but override db and use db=1


		    NOTE: Calling this function will clear the connection_pool attribute of all stored managed connections, disconnect all managed connections,
		      and close-out the connection pool.
		     It may not be safe to call this function while other threads are potentially hitting Redis (not that it would make sense anyway...)

		     @see clearRedisPools   for more info
	'''
	global _defaultRedisConnectionParams
	_defaultRedisConnectionParams.clear()

	for key, value in connectionParams.items():
		_defaultRedisConnectionParams[key] = value
	
	clearRedisPools()