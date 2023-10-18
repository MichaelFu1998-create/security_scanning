def purge_items(self):
        """Remove purged and overlimit items from the cache.

        TODO: optimize somehow.

        Leave no more than 75% of `self.max_items` items in the cache."""
        self._lock.acquire()
        try:
            il=self._items_list
            num_items = len(il)
            need_remove = num_items - int(0.75 * self.max_items)

            for _unused in range(need_remove):
                item=il.pop(0)
                try:
                    del self._items[item.address]
                except KeyError:
                    pass

            while il and il[0].update_state()=="purged":
                item=il.pop(0)
                try:
                    del self._items[item.address]
                except KeyError:
                    pass
        finally:
            self._lock.release()