def add_item(self, item):
        """Add an item to the cache.

        Item state is updated before adding it (it will not be 'new' any more).

        :Parameters:
            - `item`: the item to add.
        :Types:
            - `item`: `CacheItem`

        :return: state of the item after addition.
        :returntype: `str`
        """
        self._lock.acquire()
        try:
            state = item.update_state()
            if state != 'purged':
                if len(self._items_list) >= self.max_items:
                    self.purge_items()
                self._items[item.address] = item
                self._items_list.append(item)
                self._items_list.sort()
            return item.state
        finally:
            self._lock.release()