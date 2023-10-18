def list_characteristics(self):
        """Return list of GATT characteristics that have been discovered for this
        service.
        """
        paths = self._props.Get(_SERVICE_INTERFACE, 'Characteristics')
        return map(BluezGattCharacteristic,
                   get_provider()._get_objects_by_path(paths))