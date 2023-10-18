def wait_for_edge(self, pin, edge):
        """Wait for an edge.   Pin should be type IN.  Edge must be RISING, 
        FALLING or BOTH.
        """
        self.bbio_gpio.wait_for_edge(self.mraa_gpio.Gpio(pin), self._edge_mapping[edge])