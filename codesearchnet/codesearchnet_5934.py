def insert(self, key, obj, future_expiration_minutes=15):
        """
        Insert item into cache.

        :param key: key to look up in cache.
        :type key: ``object``

        :param obj: item to store in cache.
        :type obj: varies

        :param future_expiration_minutes: number of minutes item is valid
        :type param: ``int``

        :returns: True
        :rtype: ``bool``
        """
        expiration_time = self._calculate_expiration(future_expiration_minutes)
        self._CACHE[key] = (expiration_time, obj)
        return True