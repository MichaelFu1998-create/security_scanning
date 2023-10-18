def store(self, data, key=None, *args, **kwargs):
        """ Cache the list

            :param list data: List of objects to cache
        """
        list.__init__(self, data)
        self._store_items(self._cache_key(key))