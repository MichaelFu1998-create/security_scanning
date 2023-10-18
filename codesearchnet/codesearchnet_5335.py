def input(self,pin):
        """Read the specified pin and return HIGH/true if the pin is pulled high,
        or LOW/false if pulled low.
        """
        return self.mraa_gpio.Gpio.read(self.mraa_gpio.Gpio(pin))