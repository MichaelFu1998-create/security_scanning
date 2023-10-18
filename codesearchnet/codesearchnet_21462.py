def set_key(self, key, value, namespace=None, expire=0):
        """
        Set a key in a cache.
        :param key: Key name
        :param value: Value
        :param namespace : Namespace to associate the key with
        :param expire: expiration
        :return:
        """
        with (yield from self._pool) as redis:
            if namespace is not None:
                key = self._get_key(namespace, key)
            yield from redis.set(key, value, expire=expire)