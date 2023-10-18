def centralManager_didConnectPeripheral_(self, manager, peripheral):
        """Called when a device is connected."""
        logger.debug('centralManager_didConnectPeripheral called')
        # Setup peripheral delegate and kick off service discovery.  For now just
        # assume all services need to be discovered.
        peripheral.setDelegate_(self)
        peripheral.discoverServices_(None)
        # Fire connected event for device.
        device = device_list().get(peripheral)
        if device is not None:
            device._set_connected()