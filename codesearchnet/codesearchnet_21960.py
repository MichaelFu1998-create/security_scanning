def put(self, key, value):
        """
        >>> c = FixedSizeLRUCache(maxsize=5)
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
        >>> c.put(6, 'six')
        >>> c.size()
        5
        >>> c.get(1)
        Traceback (most recent call last):
            ...
        KeyError: 1
        >>> c.get(2)
        'two'
        >>> c.put(7, 'seven')
        >>> c.get(2)
        'two'
        >>> c.get(3)
        Traceback (most recent call last):
            ...
        KeyError: 3
        """
        # check if we're maxed out first
        if self.size() == self._maxsize:
            # need to kick something out...
            self.delete(self.last())
        LRUCache.put(self, key, value)