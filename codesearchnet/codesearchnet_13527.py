def _expire_item(self, key):
        """Do the expiration of a dictionary item.

        Remove the item if it has expired by now.

        :Parameters:
            - `key`: key to the object.
        :Types:
            - `key`: any hashable value
        """
        (timeout, callback) = self._timeouts[key]
        now = time.time()
        if timeout <= now:
            item = dict.pop(self, key)
            del self._timeouts[key]
            if callback:
                try:
                    callback(key, item)
                except TypeError:
                    try:
                        callback(key)
                    except TypeError:
                        callback()
            return None
        else:
            return timeout - now