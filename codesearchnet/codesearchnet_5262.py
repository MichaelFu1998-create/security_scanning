def set_mode(self, mode):
        """Set SPI mode which controls clock polarity and phase.  Should be a
        numeric value 0, 1, 2, or 3.  See wikipedia page for details on meaning:
        http://en.wikipedia.org/wiki/Serial_Peripheral_Interface_Bus
        """
        if mode < 0 or mode > 3:
            raise ValueError('Mode must be a value 0, 1, 2, or 3.')
        if mode & 0x02:
            # Clock is normally high in mode 2 and 3.
            self._clock_base = GPIO.HIGH
        else:
            # Clock is normally low in mode 0 and 1.
            self._clock_base = GPIO.LOW
        if mode & 0x01:
            # Read on trailing edge in mode 1 and 3.
            self._read_leading = False
        else:
            # Read on leading edge in mode 0 and 2.
            self._read_leading = True
        # Put clock into its base state.
        self._gpio.output(self._sclk, self._clock_base)