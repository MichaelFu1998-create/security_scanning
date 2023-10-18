def discover(self, service_uuids, char_uuids, timeout_sec=TIMEOUT_SEC):
        """Wait up to timeout_sec for the specified services and characteristics
        to be discovered on the device.  If the timeout is exceeded without
        discovering the services and characteristics then an exception is thrown.
        """
        # Since OSX tells us when all services and characteristics are discovered
        # this function can just wait for that full service discovery.
        if not self._discovered.wait(timeout_sec):
            raise RuntimeError('Failed to discover device services within timeout period!')