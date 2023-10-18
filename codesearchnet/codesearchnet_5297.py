def _idle(self):
        """Put I2C lines into idle state."""
        # Put the I2C lines into an idle state with SCL and SDA high.
        self._ft232h.setup_pins({0: GPIO.OUT, 1: GPIO.OUT, 2: GPIO.IN},
                                {0: GPIO.HIGH, 1: GPIO.HIGH})