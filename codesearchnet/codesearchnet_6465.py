def stop_scan(self, timeout_sec=TIMEOUT_SEC):
        """Stop scanning for BLE devices with this adapter."""
        self._scan_stopped.clear()
        self._adapter.StopDiscovery()
        if not self._scan_stopped.wait(timeout_sec):
            raise RuntimeError('Exceeded timeout waiting for adapter to stop scanning!')