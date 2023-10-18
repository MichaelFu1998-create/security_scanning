def read(self, pin):
        """Reads value from pin `pin`.

        Returns the value read from pin `pin`. If it's an analog pin, returns
        a number in analog.input_range. If it's digital, returns
        `ahio.LogicValue`.

        If you're developing a driver, implement _read(self, pin)

        @arg pin the pin to read from
        @returns the value read from the pin

        @throw KeyError if pin isn't mapped.
        """
        if type(pin) is list:
            return [self.read(p) for p in pin]

        pin_id = self._pin_mapping.get(pin, None)
        if pin_id:
            value = self._read(pin_id)
            lpin = self._pin_lin.get(pin, None)
            if lpin and type(lpin['read']) is tuple:
                read_range = lpin['read']
                value = self._linear_interpolation(value, *read_range)
            return value
        else:
            raise KeyError('Requested pin is not mapped: %s' % pin)