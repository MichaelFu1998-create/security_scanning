def delete(self, key):
        """
        >>> c = MemSizeLRUCache()
        >>> c.put(1, 1)
        >>> c.mem()
        24
        >>> c.delete(1)
        >>> c.mem()
        0
        """
        (_value, mem) = LRUCache.get(self, key)
        self._mem -= mem
        LRUCache.delete(self, key)