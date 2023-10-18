def _interrupt_read(self):
        """
        Read data from device.
        """
        data = self._device.read(ENDPOINT, REQ_INT_LEN, timeout=TIMEOUT)
        LOGGER.debug('Read data: %r', data)
        return data