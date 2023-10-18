def _i2c_stop(self):
        """Send I2C stop signal. Must be called within a transaction start/end.
        """
        # Set SCL low and SDA low for a short period.
        self._ft232h.output_pins({0: GPIO.LOW, 1: GPIO.LOW}, write=False)
        self._command.append(self._ft232h.mpsse_gpio() * _REPEAT_DELAY)
        # Set SCL high and SDA low for a short period.
        self._ft232h.output_pins({0: GPIO.HIGH, 1: GPIO.LOW}, write=False)
        self._command.append(self._ft232h.mpsse_gpio() * _REPEAT_DELAY)
        # Finally set SCL high and SDA high for a short period.
        self._ft232h.output_pins({0: GPIO.HIGH, 1: GPIO.HIGH}, write=False)
        self._command.append(self._ft232h.mpsse_gpio() * _REPEAT_DELAY)