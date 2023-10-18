def setup_pins(self, pins, values={}, write=True):
        """Setup multiple pins as inputs or outputs at once.  Pins should be a
        dict of pin name to pin mode (IN or OUT).  Optional starting values of
        pins can be provided in the values dict (with pin name to pin value).
        """
        # General implementation that can be improved by subclasses.
        for pin, mode in iter(pins.items()):
            self._setup_pin(pin, mode)
        for pin, value in iter(values.items()):
            self._output_pin(pin, value)
        if write:
            self.mpsse_write_gpio()