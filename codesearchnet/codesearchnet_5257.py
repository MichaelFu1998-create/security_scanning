def start(self, pin, dutycycle, frequency_hz=2000):
        """Enable PWM output on specified pin.  Set to intiial percent duty cycle
        value (0.0 to 100.0) and frequency (in Hz).
        """
        if dutycycle < 0.0 or dutycycle > 100.0:
            raise ValueError('Invalid duty cycle value, must be between 0.0 to 100.0 (inclusive).')
        self.bbio_pwm.start(pin, dutycycle, frequency_hz)