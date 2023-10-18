def add(self, cbobject, metadata):
        """Add the specified CoreBluetooth item with the associated metadata if
        it doesn't already exist.  Returns the newly created or preexisting
        metadata item.
        """
        with self._lock:
            if cbobject not in self._metadata:
                self._metadata[cbobject] = metadata
            return self._metadata[cbobject]