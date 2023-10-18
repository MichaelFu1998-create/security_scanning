def discover(self, service_uuids, char_uuids, timeout_sec=TIMEOUT_SEC):
        """Wait up to timeout_sec for the specified services and characteristics
        to be discovered on the device.  If the timeout is exceeded without
        discovering the services and characteristics then an exception is thrown.
        """
        # Turn expected values into a counter of each UUID for fast comparison.
        expected_services = set(service_uuids)
        expected_chars = set(char_uuids)
        # Loop trying to find the expected services for the device.
        start = time.time()
        while True:
            # Find actual services discovered for the device.
            actual_services = set(self.advertised)
            # Find actual characteristics discovered for the device.
            chars = map(BluezGattCharacteristic,
                        get_provider()._get_objects(_CHARACTERISTIC_INTERFACE,
                                                    self._device.object_path))
            actual_chars = set(map(lambda x: x.uuid, chars))
            # Compare actual discovered UUIDs with expected and return true if at
            # least the expected UUIDs are available.
            if actual_services >= expected_services and actual_chars >= expected_chars:
                # Found at least the expected services!
                return True
            # Couldn't find the devices so check if timeout has expired and try again.
            if time.time()-start >= timeout_sec:
                return False
            time.sleep(1)