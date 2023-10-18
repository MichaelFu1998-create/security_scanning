def connect(self, timeout_sec=TIMEOUT_SEC):
        """Connect to the device.  If not connected within the specified timeout
        then an exception is thrown.
        """
        self._connected.clear()
        self._device.Connect()
        if not self._connected.wait(timeout_sec):
            raise RuntimeError('Exceeded timeout waiting to connect to device!')