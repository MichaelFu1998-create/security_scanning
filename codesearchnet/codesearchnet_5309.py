def readRaw8(self):
        """Read an 8-bit value on the bus (without register)."""
        self._idle()
        self._transaction_start()
        self._i2c_start()
        self._i2c_write_bytes([self._address_byte(False)])
        self._i2c_stop()
        self._i2c_idle()
        self._i2c_start()
        self._i2c_write_bytes([self._address_byte(True)])
        self._i2c_read_bytes(1)
        self._i2c_stop()
        response = self._transaction_end()
        self._verify_acks(response[:-1])
        return response[-1]