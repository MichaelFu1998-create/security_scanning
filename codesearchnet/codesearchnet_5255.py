def set_frequency(self, pin, frequency_hz):
        """Set frequency (in Hz) of PWM output on specified pin."""
        if pin not in self.pwm:
            raise ValueError('Pin {0} is not configured as a PWM.  Make sure to first call start for the pin.'.format(pin))
        self.pwm[pin].ChangeFrequency(frequency_hz)