def set_pin_direction(self, pin, direction):
        """Sets pin `pin` to `direction`.

        The pin should support the requested mode. Calling this function
        on a unmapped pin does nothing. Calling it with a unsupported direction
        throws RuntimeError.

        If you're developing a driver, you should implement
        _set_pin_direction(self, pin, direction) where `pin` will be one of
        your internal IDs. If a pin is set to OUTPUT, put it on LOW state.

        @arg pin pin id you've set using `AbstractDriver.map_pin`
        @arg mode a value from `AbstractDriver.Direction`

        @throw KeyError if pin isn't mapped.
        @throw RuntimeError if direction is not supported by pin.
        """
        if type(pin) is list:
            for p in pin:
                self.set_pin_direction(p, direction)
            return

        pin_id = self._pin_mapping.get(pin, None)
        if pin_id and type(direction) is ahio.Direction:
            self._set_pin_direction(pin_id, direction)
        else:
            raise KeyError('Requested pin is not mapped: %s' % pin)