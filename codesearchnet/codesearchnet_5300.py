def _i2c_idle(self):
        """Set I2C signals to idle state with SCL and SDA at a high value. Must
        be called within a transaction start/end.
        """
        self._ft232h.output_pins({0: GPIO.HIGH, 1: GPIO.HIGH}, write=False)
        self._command.append(self._ft232h.mpsse_gpio() * _REPEAT_DELAY)