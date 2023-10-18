def remove(self, cbobject):
        """Remove any metadata associated with the provided CoreBluetooth object.
        """
        with self._lock:
            if cbobject in self._metadata:
                del self._metadata[cbobject]