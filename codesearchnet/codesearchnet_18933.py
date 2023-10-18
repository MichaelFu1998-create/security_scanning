def set_analog_reference(self, reference, pin=None):
        """Sets the analog reference to `reference`

        If the driver supports per pin reference setting, set pin to the
        desired reference. If not, passing None means set to all, which is the
        default in most hardware. If only per pin reference is supported and
        pin is None, raise RuntimeError.

        If you're developing a driver, implement
        _set_analog_reference(self, reference, pin). Raise RuntimeError if pin
        was set but is not supported by the platform.

        @arg reference the value that describes the analog reference. See
            `AbstractDriver.analog_references`
        @arg pin if the the driver supports it, the pin that will use
            `reference` as reference. None for all.

        @throw RuntimeError if pin is None on a per pin only hardware, or if
            it's a valid pin on a global only analog reference hardware.
        @throw KeyError if pin isn't mapped.
        """
        if pin is None:
            self._set_analog_reference(reference, None)
        else:
            pin_id = self._pin_mapping.get(pin, None)
            if pin_id:
                self._set_analog_reference(reference, pin_id)
            else:
                raise KeyError('Requested pin is not mapped: %s' % pin)