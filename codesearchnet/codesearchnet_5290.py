def input_pins(self, pins):
        """Read multiple pins specified in the given list and return list of pin values
        GPIO.HIGH/True if the pin is pulled high, or GPIO.LOW/False if pulled low."""
        if [pin for pin in pins if pin < 0 or pin > 15]:
            raise ValueError('Pin must be between 0 and 15 (inclusive).')
        _pins = self.mpsse_read_gpio()
        return [((_pins >> pin) & 0x0001) == 1 for pin in pins]