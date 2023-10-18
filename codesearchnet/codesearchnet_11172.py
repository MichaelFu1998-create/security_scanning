def encode(self, word, max_length=-1):
        """Return the PhoneticSpanish coding of word.

        Parameters
        ----------
        word : str
            The word to transform
        max_length : int
            The length of the code returned (defaults to unlimited)

        Returns
        -------
        str
            The PhoneticSpanish code

        Examples
        --------
        >>> pe = PhoneticSpanish()
        >>> pe.encode('Perez')
        '094'
        >>> pe.encode('Martinez')
        '69364'
        >>> pe.encode('Gutierrez')
        '83994'
        >>> pe.encode('Santiago')
        '4638'
        >>> pe.encode('Nicolás')
        '6454'

        """
        # uppercase, normalize, and decompose, filter to A-Z minus vowels & W
        word = unicode_normalize('NFKD', text_type(word.upper()))
        word = ''.join(c for c in word if c in self._uc_set)

        # merge repeated Ls & Rs
        word = word.replace('LL', 'L')
        word = word.replace('R', 'R')

        # apply the Soundex algorithm
        sdx = word.translate(self._trans)

        if max_length > 0:
            sdx = (sdx + ('0' * max_length))[:max_length]

        return sdx