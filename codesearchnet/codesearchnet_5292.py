def set_bit_order(self, order):
        """Set order of bits to be read/written over serial lines.  Should be
        either MSBFIRST for most-significant first, or LSBFIRST for
        least-signifcant first.
        """
        if order == MSBFIRST:
            self.lsbfirst = 0
        elif order == LSBFIRST:
            self.lsbfirst = 1
        else:
            raise ValueError('Order must be MSBFIRST or LSBFIRST.')