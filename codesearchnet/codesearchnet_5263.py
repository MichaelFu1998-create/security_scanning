def set_bit_order(self, order):
        """Set order of bits to be read/written over serial lines.  Should be
        either MSBFIRST for most-significant first, or LSBFIRST for
        least-signifcant first.
        """
        # Set self._mask to the bitmask which points at the appropriate bit to
        # read or write, and appropriate left/right shift operator function for
        # reading/writing.
        if order == MSBFIRST:
            self._mask = 0x80
            self._write_shift = operator.lshift
            self._read_shift = operator.rshift
        elif order == LSBFIRST:
            self._mask = 0x01
            self._write_shift = operator.rshift
            self._read_shift = operator.lshift
        else:
            raise ValueError('Order must be MSBFIRST or LSBFIRST.')