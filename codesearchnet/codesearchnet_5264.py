def write(self, data, assert_ss=True, deassert_ss=True):
        """Half-duplex SPI write.  If assert_ss is True, the SS line will be
        asserted low, the specified bytes will be clocked out the MOSI line, and
        if deassert_ss is True the SS line be put back high.
        """
        # Fail MOSI is not specified.
        if self._mosi is None:
            raise RuntimeError('Write attempted with no MOSI pin specified.')
        if assert_ss and self._ss is not None:
            self._gpio.set_low(self._ss)
        for byte in data:
            for i in range(8):
                # Write bit to MOSI.
                if self._write_shift(byte, i) & self._mask:
                    self._gpio.set_high(self._mosi)
                else:
                    self._gpio.set_low(self._mosi)
                # Flip clock off base.
                self._gpio.output(self._sclk, not self._clock_base)
                # Return clock to base.
                self._gpio.output(self._sclk, self._clock_base)
        if deassert_ss and self._ss is not None:
            self._gpio.set_high(self._ss)