def cleanup(self, pin=None):
        """Clean up GPIO event detection for specific pin, or all pins if none 
        is specified.
        """
        if pin is None:
            self.rpi_gpio.cleanup()
        else:
            self.rpi_gpio.cleanup(pin)