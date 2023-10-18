def set_item(self, key, value, timeout = None, timeout_callback = None):
        """Set item of the dictionary.

        :Parameters:
            - `key`: the key.
            - `value`: the object to store.
            - `timeout`: timeout value for the object (in seconds from now).
            - `timeout_callback`: function to be called when the item expires.
              The callback should accept none, one (the key) or two (the key
              and the value) arguments.
        :Types:
            - `key`: any hashable value
            - `value`: any python object
            - `timeout`: `int`
            - `timeout_callback`: callable
        """
        with self._lock:
            logger.debug("expdict.__setitem__({0!r}, {1!r}, {2!r}, {3!r})"
                            .format(key, value, timeout, timeout_callback))
            if not timeout:
                timeout = self._default_timeout
            self._timeouts[key] = (time.time() + timeout, timeout_callback)
            return dict.__setitem__(self, key, value)