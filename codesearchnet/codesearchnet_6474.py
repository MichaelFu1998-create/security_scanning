def peripheral_didUpdateValueForDescriptor_error_(self, peripheral, descriptor, error):
        """Called when descriptor value was read or updated."""
        logger.debug('peripheral_didUpdateValueForDescriptor_error called')
        # Stop if there was some kind of error.
        if error is not None:
            return
        # Notify the device about the updated descriptor value.
        device = device_list().get(peripheral)
        if device is not None:
            device._descriptor_changed(descriptor)