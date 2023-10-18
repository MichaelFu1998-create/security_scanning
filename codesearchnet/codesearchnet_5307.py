def writeList(self, register, data):
        """Write bytes to the specified register."""
        self._idle()
        self._transaction_start()
        self._i2c_start()
        self._i2c_write_bytes([self._address_byte(False), register] + data)
        self._i2c_stop()
        response = self._transaction_end()
        self._verify_acks(response)