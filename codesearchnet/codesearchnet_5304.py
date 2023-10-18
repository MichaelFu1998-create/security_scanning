def ping(self):
        """Attempt to detect if a device at this address is present on the I2C
        bus.  Will send out the device's address for writing and verify an ACK
        is received.  Returns true if the ACK is received, and false if not.
        """
        self._idle()
        self._transaction_start()
        self._i2c_start()
        self._i2c_write_bytes([self._address_byte(False)])
        self._i2c_stop()
        response = self._transaction_end()
        if len(response) != 1:
            raise RuntimeError('Expected 1 response byte but received {0} byte(s).'.format(len(response)))
        return ((response[0] & 0x01) == 0x00)