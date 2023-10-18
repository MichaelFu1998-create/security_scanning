def connect(self, timeout_sec=TIMEOUT_SEC):
        """Connect to the device.  If not connected within the specified timeout
        then an exception is thrown.
        """
        self._central_manager.connectPeripheral_options_(self._peripheral, None)
        if not self._connected.wait(timeout_sec):
            raise RuntimeError('Failed to connect to device within timeout period!')