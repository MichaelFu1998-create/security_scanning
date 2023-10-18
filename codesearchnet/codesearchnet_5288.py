def output(self, pin, value):
        """Set the specified pin the provided high/low value.  Value should be
        either HIGH/LOW or a boolean (true = high)."""
        if pin < 0 or pin > 15:
            raise ValueError('Pin must be between 0 and 15 (inclusive).')
        self._output_pin(pin, value)
        self.mpsse_write_gpio()