def read_value(self):
        """Read the value of this descriptor."""
        pass
        # Kick off a query to read the value of the descriptor, then wait
        # for the result to return asyncronously.
        self._value_read.clear()
        self._device._peripheral.readValueForDescriptor(self._descriptor)
        if not self._value_read.wait(timeout_sec):
            raise RuntimeError('Exceeded timeout waiting to read characteristic value!')
        return self._value