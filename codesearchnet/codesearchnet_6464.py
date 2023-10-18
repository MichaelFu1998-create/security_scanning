def start_scan(self, timeout_sec=TIMEOUT_SEC):
        """Start scanning for BLE devices with this adapter."""
        self._scan_started.clear()
        self._adapter.StartDiscovery()
        if not self._scan_started.wait(timeout_sec):
            raise RuntimeError('Exceeded timeout waiting for adapter to start scanning!')