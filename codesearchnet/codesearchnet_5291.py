def set_mode(self, mode):
        """Set SPI mode which controls clock polarity and phase.  Should be a
        numeric value 0, 1, 2, or 3.  See wikipedia page for details on meaning:
        http://en.wikipedia.org/wiki/Serial_Peripheral_Interface_Bus
        """
        if mode < 0 or mode > 3:
            raise ValueError('Mode must be a value 0, 1, 2, or 3.')
        if mode == 0:
            # Mode 0 captures on rising clock, propagates on falling clock
            self.write_clock_ve = 1
            self.read_clock_ve  = 0
            # Clock base is low.
            clock_base = GPIO.LOW
        elif mode == 1:
            # Mode 1 capture of falling edge, propagate on rising clock
            self.write_clock_ve = 0
            self.read_clock_ve  = 1
            # Clock base is low.
            clock_base = GPIO.LOW
        elif mode == 2:
            # Mode 2 capture on rising clock, propagate on falling clock
            self.write_clock_ve = 1
            self.read_clock_ve  = 0
            # Clock base is high.
            clock_base = GPIO.HIGH
        elif mode == 3:
            # Mode 3 capture on falling edge, propagage on rising clock
            self.write_clock_ve = 0
            self.read_clock_ve  = 1
            # Clock base is high.
            clock_base = GPIO.HIGH
        # Set clock and DO as output, DI as input.  Also start clock at its base value.
        self._ft232h.setup_pins({0: GPIO.OUT, 1: GPIO.OUT, 2: GPIO.IN}, {0: clock_base})