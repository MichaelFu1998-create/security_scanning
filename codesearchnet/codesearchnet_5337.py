def remove_event_detect(self, pin):
        """Remove edge detection for a particular GPIO channel.  Pin should be
        type IN.
        """
        self.mraa_gpio.Gpio.isrExit(self.mraa_gpio.Gpio(pin))