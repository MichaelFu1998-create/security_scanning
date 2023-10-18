def pin_type(self, pin):
        """Gets the `ahio.PortType` this pin was set to.

        If you're developing a driver, implement _pin_type(self, pin)

        @arg pin the pin you want to see the mode
        @returns the `ahio.PortType` the pin is set to

        @throw KeyError if pin isn't mapped.
        """
        if type(pin) is list:
            return [self.pin_type(p) for p in pin]

        pin_id = self._pin_mapping.get(pin, None)
        if pin_id:
            return self._pin_type(pin_id)
        else:
            raise KeyError('Requested pin is not mapped: %s' % pin)