def put(self, key, value):
        """
        >>> c = MemSizeLRUCache(maxmem=24*4)
        >>> c.put(1, 1)
        >>> c.mem() # 24-bytes per integer
        24
        >>> c.put(2, 2)
        >>> c.put(3, 3)
        >>> c.put(4, 4)
        >>> c.get(1)
        1
        >>> c.mem()
        96
        >>> c.size()
        4
        >>> c.put(5, 5)
        >>> c.size()
        4
        >>> c.get(2)
        Traceback (most recent call last):
            ...
        KeyError: 2
        """
        mem = sys.getsizeof(value)
        if self._mem + mem > self._maxmem:
            self.delete(self.last())
        LRUCache.put(self, key, (value, mem))
        self._mem += mem