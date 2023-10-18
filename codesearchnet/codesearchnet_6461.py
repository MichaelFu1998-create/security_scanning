def write_value(self, value, write_type=0):
        """Write the specified value to this characteristic."""
        data = NSData.dataWithBytes_length_(value, len(value))
        self._device._peripheral.writeValue_forCharacteristic_type_(data,
            self._characteristic,
            write_type)