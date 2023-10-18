def get_all(self, cbobjects):
        """Retrieve a list of metadata objects associated with the specified
        list of CoreBluetooth objects.  If an object cannot be found then an
        exception is thrown.
        """
        try:
            with self._lock:
                return [self._metadata[x] for x in cbobjects]
        except KeyError:
            # Note that if this error gets thrown then the assumption that OSX
            # will pass back to callbacks the exact CoreBluetooth objects that
            # were used previously is broken! (i.e. the CoreBluetooth objects
            # are not stateless)
            raise RuntimeError('Failed to find expected metadata for CoreBluetooth object!')