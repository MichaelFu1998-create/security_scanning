def delete(self, key):
        """
        >>> c = LRUCache()
        >>> c.put(1, 'one')
        >>> c.get(1)
        'one'
        >>> c.delete(1)
        >>> c.get(1)
        Traceback (most recent call last):
            ...
        KeyError: 1
        >>> c.delete(1)
        Traceback (most recent call last):
            ...
        KeyError: 1
        """
        del self._cache[key]
        self._order.delete(key)
        self._size -= 1