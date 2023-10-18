def rssi(self, timeout_sec=TIMEOUT_SEC):
        """Return the RSSI signal strength in decibels."""
        # Kick off query to get RSSI, then wait for it to return asyncronously
        # when the _rssi_changed() function is called.
        self._rssi_read.clear()
        self._peripheral.readRSSI()
        if not self._rssi_read.wait(timeout_sec):
            raise RuntimeError('Exceeded timeout waiting for RSSI value!')
        return self._rssi