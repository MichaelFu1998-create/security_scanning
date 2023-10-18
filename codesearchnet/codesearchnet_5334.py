def output(self,pin,value):
        """Set the specified pin the provided high/low value.  Value should be
        either 1 (ON or HIGH), or 0 (OFF or LOW) or a boolean.
        """
        self.mraa_gpio.Gpio.write(self.mraa_gpio.Gpio(pin), value)