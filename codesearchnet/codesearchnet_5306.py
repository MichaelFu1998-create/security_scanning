def write16(self, register, value, little_endian=True):
        """Write a 16-bit value to the specified register."""
        value = value & 0xFFFF
        value_low  = value & 0xFF
        value_high = (value >> 8) & 0xFF
        if not little_endian:
            value_low, value_high = value_high, value_low
        self._idle()
        self._transaction_start()
        self._i2c_start()
        self._i2c_write_bytes([self._address_byte(False), register, value_low,
                                value_high])
        self._i2c_stop()
        response = self._transaction_end()
        self._verify_acks(response)