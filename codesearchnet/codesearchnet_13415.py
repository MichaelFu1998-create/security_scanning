def invalidate_object(self, address, state = 'stale'):
        """Force cache item state change (to 'worse' state only).

        :Parameters:
            - `state`: the new state requested.
        :Types:
            - `state`: `str`"""
        self._lock.acquire()
        try:
            item = self.get_item(address)
            if item and item.state_value<_state_values[state]:
                item.state=state
                item.update_state()
                self._items_list.sort()
        finally:
            self._lock.release()