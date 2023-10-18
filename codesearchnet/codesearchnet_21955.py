def get(self, key):
        """
        >>> c = LRUCache()
        >>> c.get('toto')
        Traceback (most recent call last):
            ...
        KeyError: 'toto'
        >>> c.stats()['misses']
        1
        >>> c.put('toto', 'tata')
        >>> c.get('toto')
        'tata'
        >>> c.stats()['hits']
        1
        """
        try:
            value = self._cache[key]
            self._order.push(key)
            self._hits += 1
            return value
        except KeyError, e:
            self._misses += 1
            raise