def list_services(self):
        """Return a list of GattService objects that have been discovered for
        this device.
        """
        return map(BluezGattService,
                   get_provider()._get_objects(_SERVICE_INTERFACE,
                                               self._device.object_path))