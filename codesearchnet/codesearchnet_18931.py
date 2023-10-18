def write(self, pin, value, pwm=False):
        """Sets the output to the given value.

        Sets `pin` output to given value. If the pin is in INPUT mode, do
        nothing. If it's an analog pin, value should be in write_range.
        If it's not in the allowed range, it will be clamped. If pin is in
        digital mode, value can be `ahio.LogicValue` if `pwm` = False, or a
        number between 0 and 1 if `pwm` = True. If PWM is False, the pin will
        be set to HIGH or LOW, if `pwm` is True, a PWM wave with the given
        cycle will be created. If the pin does not support PWM and `pwm` is
        True, raise RuntimeError. The `pwm` argument should be ignored in case
        the pin is analog. If value is not valid for the given
        pwm/analog|digital combination, raise TypeError.

        If you're developing a driver, implement _write(self, pin, value, pwm)

        @arg pin the pin to write to
        @arg value the value to write on the pin
        @arg pwm wether the output should be a pwm wave

        @throw RuntimeError if the pin does not support PWM and `pwm` is True.
        @throw TypeError if value is not valid for this pin's mode and pwm
               value.
        @throw KeyError if pin isn't mapped.
        """
        if type(pin) is list:
            for p in pin:
                self.write(p, value, pwm)
            return

        if pwm and type(value) is not int and type(value) is not float:
            raise TypeError('pwm is set, but value is not a float or int')

        pin_id = self._pin_mapping.get(pin, None)
        if pin_id:
            lpin = self._pin_lin.get(pin, None)
            if lpin and type(lpin['write']) is tuple:
                write_range = lpin['write']
                value = self._linear_interpolation(value, *write_range)
            self._write(pin_id, value, pwm)
        else:
            raise KeyError('Requested pin is not mapped: %s' % pin)