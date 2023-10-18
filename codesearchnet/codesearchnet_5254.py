def set_duty_cycle(self, pin, dutycycle):
        """Set percent duty cycle of PWM output on specified pin.  Duty cycle must
        be a value 0.0 to 100.0 (inclusive).
        """
        if dutycycle < 0.0 or dutycycle > 100.0:
            raise ValueError('Invalid duty cycle value, must be between 0.0 to 100.0 (inclusive).')
        if pin not in self.pwm:
            raise ValueError('Pin {0} is not configured as a PWM.  Make sure to first call start for the pin.'.format(pin))
        self.pwm[pin].ChangeDutyCycle(dutycycle)