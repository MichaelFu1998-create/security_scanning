def _i2c_write_bytes(self, data):
        """Write the specified number of bytes to the chip."""
        for byte in data:
            # Write byte.
            self._command.append(str(bytearray((0x11, 0x00, 0x00, byte))))
            # Make sure pins are back in idle state with clock low and data high.
            self._ft232h.output_pins({0: GPIO.LOW, 1: GPIO.HIGH}, write=False)
            self._command.append(self._ft232h.mpsse_gpio() * _REPEAT_DELAY)
            # Read bit for ACK/NAK.
            self._command.append('\x22\x00')
        # Increase expected response bytes.
        self._expected += len(data)