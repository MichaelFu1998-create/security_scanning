def close(self):
        """Close the FTDI device.  Will be automatically called when the program ends."""
        if self._ctx is not None:
            ftdi.free(self._ctx)
        self._ctx = None