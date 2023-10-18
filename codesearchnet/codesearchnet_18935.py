def set_pwm_frequency(self, frequency, pin=None):
        """Sets PWM frequency, if supported by hardware

        If the driver supports per pin frequency setting, set pin to the
        desired frequency. If not, passing None means set to all. If only per
        pin frequency is supported and pin is None, raise RuntimeError.

        If you're developing a driver, implement
        _set_pwm_frequency(self, frequency, pin). Raise RuntimeError if pin
        was set but is not supported by the platform.

        @arg frequency pwm frequency to be set, in Hz
        @arg pin if the the driver supports it, the pin that will use
            `frequency` as pwm frequency. None for all/global.

        @throw RuntimeError if pin is None on a per pin only hardware, or if
            it's a valid pin on a global only hardware.
        @throw KeyError if pin isn't mapped.
        """
        if pin is None:
            self._set_pwm_frequency(frequency, None)
        else:
            pin_id = self._pin_mapping.get(pin, None)
            if pin_id:
                self._set_pwm_frequency(frequency, pin_id)
            else:
                raise KeyError('Requested pin is not mapped: %s' % pin)