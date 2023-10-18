def read(self, length, assert_ss=True, deassert_ss=True):
        """Half-duplex SPI read.  If assert_ss is true, the SS line will be
        asserted low, the specified length of bytes will be clocked in the MISO
        line, and if deassert_ss is true the SS line will be put back high.
        Bytes which are read will be returned as a bytearray object.
        """
        if self._miso is None:
            raise RuntimeError('Read attempted with no MISO pin specified.')
        if assert_ss and self._ss is not None:
            self._gpio.set_low(self._ss)
        result = bytearray(length)
        for i in range(length):
            for j in range(8):
                # Flip clock off base.
                self._gpio.output(self._sclk, not self._clock_base)
                # Handle read on leading edge of clock.
                if self._read_leading:
                    if self._gpio.is_high(self._miso):
                        # Set bit to 1 at appropriate location.
                        result[i] |= self._read_shift(self._mask, j)
                    else:
                        # Set bit to 0 at appropriate location.
                        result[i] &= ~self._read_shift(self._mask, j)
                # Return clock to base.
                self._gpio.output(self._sclk, self._clock_base)
                # Handle read on trailing edge of clock.
                if not self._read_leading:
                    if self._gpio.is_high(self._miso):
                        # Set bit to 1 at appropriate location.
                        result[i] |= self._read_shift(self._mask, j)
                    else:
                        # Set bit to 0 at appropriate location.
                        result[i] &= ~self._read_shift(self._mask, j)
        if deassert_ss and self._ss is not None:
            self._gpio.set_high(self._ss)
        return result