def start_scan(self, timeout_sec=TIMEOUT_SEC):
        """Start scanning for BLE devices."""
        get_provider()._central_manager.scanForPeripheralsWithServices_options_(None, None)
        self._is_scanning = True