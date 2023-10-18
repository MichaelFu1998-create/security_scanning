def centralManager_didDiscoverPeripheral_advertisementData_RSSI_(self, manager, peripheral, data, rssi):
        """Called when the BLE adapter found a device while scanning, or has
        new advertisement data for a device.
        """
        logger.debug('centralManager_didDiscoverPeripheral_advertisementData_RSSI called')
        # Log name of device found while scanning.
        #logger.debug('Saw device advertised with name: {0}'.format(peripheral.name()))
        # Make sure the device is added to the list of devices and then update
        # its advertisement state.
        device = device_list().get(peripheral)
        if device is None:
            device = device_list().add(peripheral, CoreBluetoothDevice(peripheral))
        device._update_advertised(data)