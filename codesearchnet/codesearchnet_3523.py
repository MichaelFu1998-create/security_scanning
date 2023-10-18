def sync(f):
    """ Synchronization decorator. """

    def new_function(self, *args, **kw):
        self._lock.acquire()
        try:
            return f(self, *args, **kw)
        finally:
            self._lock.release()
    return new_function