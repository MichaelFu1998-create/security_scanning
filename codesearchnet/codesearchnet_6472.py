def peripheral_didDiscoverDescriptorsForCharacteristic_error_(self, peripheral, characteristic, error):
        """Called when characteristics are discovered for a service."""
        logger.debug('peripheral_didDiscoverDescriptorsForCharacteristic_error called')
        # Stop if there was some kind of error.
        if error is not None:
            return
        # Make sure the discovered descriptors are added to the list of known
        # descriptors.
        for desc in characteristic.descriptors():
            # Add to list of known descriptors.
            if descriptor_list().get(desc) is None:
                descriptor_list().add(desc, CoreBluetoothGattDescriptor(desc))