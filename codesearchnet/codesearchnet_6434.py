def disconnect(self, timeout_sec=TIMEOUT_SEC):
        """Disconnect from the device.  If not disconnected within the specified
        timeout then an exception is thrown.
        """
        # Remove all the services, characteristics, and descriptors from the
        # lists of those items.  Do this before disconnecting because they wont't
        # be accessible afterwards.
        for service in self.list_services():
            for char in service.list_characteristics():
                for desc in char.list_descriptors():
                    descriptor_list().remove(desc)
                characteristic_list().remove(char)
            service_list().remove(service)
        # Now disconnect.
        self._central_manager.cancelPeripheralConnection_(self._peripheral)
        if not self._disconnected.wait(timeout_sec):
            raise RuntimeError('Failed to disconnect to device within timeout period!')