def setup(self, pin, value):
        """Set the input or output mode for a specified pin.  Mode should be
        either GPIO.OUT or GPIO.IN.
        """
        self._validate_pin(pin)
        # Set bit to 1 for input or 0 for output.
        if value == GPIO.IN:
            self.iodir[int(pin/8)] |= 1 << (int(pin%8))
        elif value == GPIO.OUT:
            self.iodir[int(pin/8)] &= ~(1 << (int(pin%8)))
        else:
            raise ValueError('Unexpected value.  Must be GPIO.IN or GPIO.OUT.')
        self.write_iodir()