def store(self, data, key="id"):
        """ Cache the list

            :param list data: List of objects to cache
        """
        dict.__init__(self, data)
        self._store_item(key)