def get_item(self, address, state = 'fresh'):
        """Get an item from the cache.

        :Parameters:
            - `address`: its address.
            - `state`: the worst state that is acceptable.
        :Types:
            - `address`: any hashable
            - `state`: `str`

        :return: the item or `None` if it was not found.
        :returntype: `CacheItem`"""
        self._lock.acquire()
        try:
            item = self._items.get(address)
            if not item:
                return None
            self.update_item(item)
            if _state_values[state] >= item.state_value:
                return item
            return None
        finally:
            self._lock.release()