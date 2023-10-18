def fingerprint(self, word, n_bits=16, most_common=MOST_COMMON_LETTERS_CG):
        """Return the count fingerprint.

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
            The count fingerprint

        Examples
        --------
        >>> cf = Count()
        >>> bin(cf.fingerprint('hat'))
        '0b1010000000001'
        >>> bin(cf.fingerprint('niall'))
        '0b10001010000'
        >>> bin(cf.fingerprint('colin'))
        '0b101010000'
        >>> bin(cf.fingerprint('atcg'))
        '0b1010000000000'
        >>> bin(cf.fingerprint('entreatment'))
        '0b1111010000100000'

        """
        if n_bits % 2:
            n_bits += 1

        word = Counter(word)
        fingerprint = 0

        for letter in most_common:
            if n_bits:
                fingerprint <<= 2
                fingerprint += word[letter] & 3
                n_bits -= 2
            else:
                break

        if n_bits:
            fingerprint <<= n_bits

        return fingerprint