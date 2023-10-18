def list_descriptors(self):
        """Return list of GATT descriptors that have been discovered for this
        characteristic.
        """
        paths = self._props.Get(_CHARACTERISTIC_INTERFACE, 'Descriptors')
        return map(BluezGattDescriptor,
                   get_provider()._get_objects_by_path(paths))