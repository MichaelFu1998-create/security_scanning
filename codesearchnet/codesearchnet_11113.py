def decode(self, longval, nbits):
        """Decode the number to a string using the given statistics.

        Parameters
        ----------
        longval : int
            The first part of an encoded tuple from encode
        nbits : int
            The second part of an encoded tuple from encode

        Returns
        -------
        str
            The arithmetically decoded text

        Example
        -------
        >>> ac = Arithmetic('the quick brown fox jumped over the lazy dog')
        >>> ac.decode(16720586181, 34)
        'align'

        """
        val = Fraction(longval, long(1) << nbits)
        letters = []

        probs_items = [
            (char, minval, maxval)
            for (char, (minval, maxval)) in self._probs.items()
        ]

        char = '\x00'
        while True:
            for (char, minval, maxval) in probs_items:  # noqa: B007
                if minval <= val < maxval:
                    break

            if char == '\x00':
                break
            letters.append(char)
            delta = maxval - minval
            val = (val - minval) / delta
        return ''.join(letters)