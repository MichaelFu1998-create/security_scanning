def disconnect_devices(self, service_uuids):
        """Disconnect any connected devices that have any of the specified
        service UUIDs.
        """
        # Get list of connected devices with specified services.
        cbuuids = map(uuid_to_cbuuid, service_uuids)
        for device in self._central_manager.retrieveConnectedPeripheralsWithServices_(cbuuids):
            self._central_manager.cancelPeripheralConnection_(device)