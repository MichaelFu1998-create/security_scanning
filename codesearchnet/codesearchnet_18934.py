def analog_reference(self, pin=None):
        """Returns the analog reference.

        If the driver supports per pin analog reference setting, returns the
        reference for pin `pin`. If pin is None, returns the global analog
        reference. If only per pin reference is supported and pin is None,
        raise RuntimeError.

        If you're developing a driver, implement _analog_reference(self, pin)

        @arg pin if the the driver supports it, the pin that will use
            `reference` as reference. None for all.

        @returns the reference used for pin

        @throw RuntimeError if pin is None on a per pin only hardware, or if
            it's a valid pin on a global only analog reference hardware.
        @throw KeyError if pin isn't mapped.
        """
        if pin is None:
            return self._analog_reference(None)
        else:
            pin_id = self._pin_mapping.get(pin, None)
            if pin_id:
                return self._analog_reference(pin_id)
            else:
                raise KeyError('Requested pin is not mapped: %s' % pin)