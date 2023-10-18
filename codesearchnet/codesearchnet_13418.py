def update_item(self, item):
        """Update state of an item in the cache.

        Update item's state and remove the item from the cache
        if its new state is 'purged'

        :Parameters:
            - `item`: item to update.
        :Types:
            - `item`: `CacheItem`

        :return: new state of the item.
        :returntype: `str`"""

        self._lock.acquire()
        try:
            state = item.update_state()
            self._items_list.sort()
            if item.state == 'purged':
                self._purged += 1
                if self._purged > 0.25*self.max_items:
                    self.purge_items()
            return state
        finally:
            self._lock.release()