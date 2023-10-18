def got_it(self, value, state = "new"):
        """Handle a successfull retrieval and call apriopriate handler.

        Should be called when retrieval succeeds.

        Do nothing when the fetcher is not active any more (after
        one of handlers was already called).

        :Parameters:
            - `value`: fetched object.
            - `state`: initial state of the object.
        :Types:
            - `value`: any
            - `state`: `str`"""
        if not self.active:
            return
        item = CacheItem(self.address, value, self._item_freshness_period,
                self._item_expiration_period, self._item_purge_period, state)
        self._object_handler(item.address, item.value, item.state)
        self.cache.add_item(item)
        self._deactivate()