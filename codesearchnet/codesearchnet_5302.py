def _i2c_read_bytes(self, length=1):
        """Read the specified number of bytes from the I2C bus.  Length is the
        number of bytes to read (must be 1 or more).
        """
        for i in range(length-1):
            # Read a byte and send ACK.
            self._command.append('\x20\x00\x00\x13\x00\x00')
            # Make sure pins are back in idle state with clock low and data high.
            self._ft232h.output_pins({0: GPIO.LOW, 1: GPIO.HIGH}, write=False)
            self._command.append(self._ft232h.mpsse_gpio())
        # Read last byte and send NAK.
        self._command.append('\x20\x00\x00\x13\x00\xFF')
        # Make sure pins are back in idle state with clock low and data high.
        self._ft232h.output_pins({0: GPIO.LOW, 1: GPIO.HIGH}, write=False)
        self._command.append(self._ft232h.mpsse_gpio())
        # Increase expected number of bytes.
        self._expected += length