def readList(self, register, length):
        """Read a length number of bytes from the specified register.  Results
        will be returned as a bytearray."""
        if length <= 0:
            raise ValueError("Length must be at least 1 byte.")
        self._idle()
        self._transaction_start()
        self._i2c_start()
        self._i2c_write_bytes([self._address_byte(True), register])
        self._i2c_stop()
        self._i2c_idle()
        self._i2c_start()
        self._i2c_read_bytes(length)
        self._i2c_stop()
        response = self._transaction_end()
        self._verify_acks(response[:-length])
        return response[-length:]