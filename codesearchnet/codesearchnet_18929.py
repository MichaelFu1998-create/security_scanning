def set_pin_type(self, pin, ptype):
        """Sets pin `pin` to `type`.

        The pin should support the requested mode. Calling this function
        on a unmapped pin does nothing. Calling it with a unsupported mode
        throws RuntimeError.

        If you're developing a driver, you should implement
        _set_pin_type(self, pin, ptype) where `pin` will be one of your
        internal IDs. If a pin is set to OUTPUT, put it on LOW state.

        @arg pin pin id you've set using `AbstractDriver.map_pin`
        @arg mode a value from `AbstractDriver.PortType`

        @throw KeyError if pin isn't mapped.
        @throw RuntimeError if type is not supported by pin.
        """
        if type(pin) is list:
            for p in pin:
                self.set_pin_type(p, ptype)
            return

        pin_id = self._pin_mapping.get(pin, None)
        if type(ptype) is not ahio.PortType:
            raise KeyError('ptype must be of type ahio.PortType')
        elif pin_id:
            self._set_pin_type(pin_id, ptype)
        else:
            raise KeyError('Requested pin is not mapped: %s' % pin)