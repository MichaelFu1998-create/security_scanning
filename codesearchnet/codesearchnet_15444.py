def get(self, key, default=_sentinel):
        """
        Gets the value from the key.
        If the key doesn't exist, the default value is returned, otherwise None.

        :param key: The key
        :param default: The default value
        :return: The value
        """
        tup = self._data.get(key.lower())
        if tup is not None:
            return tup[1]
        elif default is not _sentinel:
            return default
        else:
            return None