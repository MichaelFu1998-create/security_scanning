def peripheral_didUpdateValueForCharacteristic_error_(self, peripheral, characteristic, error):
        """Called when characteristic value was read or updated."""
        logger.debug('peripheral_didUpdateValueForCharacteristic_error called')
        # Stop if there was some kind of error.
        if error is not None:
            return
        # Notify the device about the updated characteristic value.
        device = device_list().get(peripheral)
        if device is not None:
            device._characteristic_changed(characteristic)