def setup(self, pin, mode):
        """Set the input or output mode for a specified pin.  Mode should be
        either OUT or IN."""
        self._setup_pin(pin, mode)
        self.mpsse_write_gpio()