def centralManager_didDisconnectPeripheral_error_(self, manager, peripheral, error):
        """Called when a device is disconnected."""
        logger.debug('centralManager_didDisconnectPeripheral called')
        # Get the device and remove it from the device list, then fire its
        # disconnected event.
        device = device_list().get(peripheral)
        if device is not None:
            # Fire disconnected event and remove device from device list.
            device._set_disconnected()
            device_list().remove(peripheral)