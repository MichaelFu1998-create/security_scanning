def put(self, key, value):
        """
        >>> c = LRUCache()
        >>> c.put(1, 'one')
        >>> c.get(1)
        'one'
        >>> c.size()
        1
        >>> c.put(2, 'two')
        >>> c.put(3, 'three')
        >>> c.put(4, 'four')
        >>> c.put(5, 'five')
        >>> c.get(5)
        'five'
        >>> c.size()
        5
        """
        self._cache[key] = value
        self._order.push(key)
        self._size += 1