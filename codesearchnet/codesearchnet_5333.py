def setup(self,pin,mode):
        """Set the input or output mode for a specified pin.  Mode should be
        either DIR_IN or DIR_OUT.
        """
        self.mraa_gpio.Gpio.dir(self.mraa_gpio.Gpio(pin),self._dir_mapping[mode])