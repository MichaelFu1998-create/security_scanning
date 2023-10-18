def pop(self, key, default=_sentinel):
        """
        Removes the specified key and returns the corresponding value.
        If key is not found, the default is returned if given, otherwise KeyError is raised.

        :param key: The key
        :param default: The default value
        :return: The value
        """
        if default is not _sentinel:
            tup = self._data.pop(key.lower(), default)
        else:
            tup = self._data.pop(key.lower())
        if tup is not default:
            return tup[1]
        else:
            return default