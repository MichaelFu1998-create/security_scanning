def _i2c_start(self):
        """Send I2C start signal. Must be called within a transaction start/end.
        """
        # Set SCL high and SDA low, repeat 4 times to stay in this state for a
        # short period of time.
        self._ft232h.output_pins({0: GPIO.HIGH, 1: GPIO.LOW}, write=False)
        self._command.append(self._ft232h.mpsse_gpio() * _REPEAT_DELAY)
        # Now drop SCL to low (again repeat 4 times for short delay).
        self._ft232h.output_pins({0: GPIO.LOW, 1: GPIO.LOW}, write=False)
        self._command.append(self._ft232h.mpsse_gpio() * _REPEAT_DELAY)