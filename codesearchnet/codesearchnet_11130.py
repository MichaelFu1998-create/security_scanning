def fingerprint(self, word, n_bits=16, most_common=MOST_COMMON_LETTERS_CG):
        """Return the occurrence fingerprint.

        Parameters
        ----------
        word : str
            The word to fingerprint
        n_bits : int
            Number of bits in the fingerprint returned
        most_common : list
            The most common tokens in the target language, ordered by frequency

        Returns
        -------
        int
            The occurrence fingerprint

        Examples
        --------
        >>> of = Occurrence()
        >>> bin(of.fingerprint('hat'))
        '0b110000100000000'
        >>> bin(of.fingerprint('niall'))
        '0b10110000100000'
        >>> bin(of.fingerprint('colin'))
        '0b1110000110000'
        >>> bin(of.fingerprint('atcg'))
        '0b110000000010000'
        >>> bin(of.fingerprint('entreatment'))
        '0b1110010010000100'

        """
        word = set(word)
        fingerprint = 0

        for letter in most_common:
            if letter in word:
                fingerprint += 1
            n_bits -= 1
            if n_bits:
                fingerprint <<= 1
            else:
                break

        n_bits -= 1
        if n_bits > 0:
            fingerprint <<= n_bits

        return fingerprint