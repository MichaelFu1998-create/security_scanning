def stop_scan(self, timeout_sec=TIMEOUT_SEC):
        """Stop scanning for BLE devices."""
        get_provider()._central_manager.stopScan()
        self._is_scanning = False