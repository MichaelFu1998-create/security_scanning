def read_value(self, timeout_sec=TIMEOUT_SEC):
        """Read the value of this characteristic."""
        # Kick off a query to read the value of the characteristic, then wait
        # for the result to return asyncronously.
        self._value_read.clear()
        self._device._peripheral.readValueForCharacteristic_(self._characteristic)
        if not self._value_read.wait(timeout_sec):
            raise RuntimeError('Exceeded timeout waiting to read characteristic value!')
        return self._characteristic.value()