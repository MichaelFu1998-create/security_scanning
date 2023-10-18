def encode(self, text):
        """Encode a text using arithmetic coding.

        Text and the 0-order probability statistics -> longval, nbits

        The encoded number is Fraction(longval, 2**nbits)

        Parameters
        ----------
        text : str
            A string to encode

        Returns
        -------
        tuple
            The arithmetically coded text

        Example
        -------
        >>> ac = Arithmetic('the quick brown fox jumped over the lazy dog')
        >>> ac.encode('align')
        (16720586181, 34)

        """
        text = text_type(text)
        if '\x00' in text:
            text = text.replace('\x00', ' ')
        minval = Fraction(0)
        maxval = Fraction(1)

        for char in text + '\x00':
            prob_range = self._probs[char]
            delta = maxval - minval
            maxval = minval + prob_range[1] * delta
            minval = minval + prob_range[0] * delta

        # I tried without the /2 just to check.  Doesn't work.
        # Keep scaling up until the error range is >= 1.  That
        # gives me the minimum number of bits needed to resolve
        # down to the end-of-data character.
        delta = (maxval - minval) / 2
        nbits = long(0)
        while delta < 1:
            nbits += 1
            delta *= 2
        # The below condition shouldn't ever be false
        if nbits == 0:  # pragma: no cover
            return 0, 0
        # using -1 instead of /2
        avg = (maxval + minval) * 2 ** (nbits - 1)
        # Could return a rational instead ...
        # the division truncation is deliberate
        return avg.numerator // avg.denominator, nbits