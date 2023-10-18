def disconnect(self, timeout_sec=TIMEOUT_SEC):
        """Disconnect from the device.  If not disconnected within the specified
        timeout then an exception is thrown.
        """
        self._disconnected.clear()
        self._device.Disconnect()
        if not self._disconnected.wait(timeout_sec):
            raise RuntimeError('Exceeded timeout waiting to disconnect from device!')