def acquire(self, *args, **kwargs):
        """ Wraps Lock.acquire """
        with self._stat_lock:
            self._waiting += 1

        self._lock.acquire(*args, **kwargs)

        with self._stat_lock:
            self._locked = True
            self._waiting -= 1