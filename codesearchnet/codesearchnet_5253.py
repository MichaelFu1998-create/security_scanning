def start(self, pin, dutycycle, frequency_hz=2000):
        """Enable PWM output on specified pin.  Set to intiial percent duty cycle
        value (0.0 to 100.0) and frequency (in Hz).
        """
        if dutycycle < 0.0 or dutycycle > 100.0:
            raise ValueError('Invalid duty cycle value, must be between 0.0 to 100.0 (inclusive).')
        # Make pin an output.
        self.rpi_gpio.setup(pin, self.rpi_gpio.OUT)
        # Create PWM instance and save a reference for later access.
        self.pwm[pin] = self.rpi_gpio.PWM(pin, frequency_hz)
        # Start the PWM at the specified duty cycle.
        self.pwm[pin].start(dutycycle)