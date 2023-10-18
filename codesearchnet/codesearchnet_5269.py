def input_pins(self, pins):
        """Read multiple pins specified in the given list and return list of pin values
        GPIO.HIGH/True if the pin is pulled high, or GPIO.LOW/False if pulled low.
        """
        [self._validate_pin(pin) for pin in pins]
        # Get GPIO state.
        self.gpio = self._device.readList(self.GPIO, self.gpio_bytes)
        # Return True if pin's bit is set.
        return [(self.gpio[int(pin/8)] & 1 << (int(pin%8))) > 0 for pin in pins]