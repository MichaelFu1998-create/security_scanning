def peripheral_didDiscoverCharacteristicsForService_error_(self, peripheral, service, error):
        """Called when characteristics are discovered for a service."""
        logger.debug('peripheral_didDiscoverCharacteristicsForService_error called')
        # Stop if there was some kind of error.
        if error is not None:
            return
        # Make sure the discovered characteristics are added to the list of known
        # characteristics, and kick off descriptor discovery for each char.
        for char in service.characteristics():
            # Add to list of known characteristics.
            if characteristic_list().get(char) is None:
                characteristic_list().add(char, CoreBluetoothGattCharacteristic(char))
            # Start descriptor discovery.
            peripheral.discoverDescriptorsForCharacteristic_(char)
        # Notify the device about the discovered characteristics.
        device = device_list().get(peripheral)
        if device is not None:
            device._characteristics_discovered(service)