def fingerprint(
        self,
        word,
        n_bits=16,
        most_common=MOST_COMMON_LETTERS_CG,
        bits_per_letter=3,
    ):
        """Return the position fingerprint.

        Parameters
        ----------
        word : str
            The word to fingerprint
        n_bits : int
            Number of bits in the fingerprint returned
        most_common : list
            The most common tokens in the target language, ordered by frequency
        bits_per_letter : int
            The bits to assign for letter position

        Returns
        -------
        int
            The position fingerprint

        Examples
        --------
        >>> bin(position_fingerprint('hat'))
        '0b1110100011111111'
        >>> bin(position_fingerprint('niall'))
        '0b1111110101110010'
        >>> bin(position_fingerprint('colin'))
        '0b1111111110010111'
        >>> bin(position_fingerprint('atcg'))
        '0b1110010001111111'
        >>> bin(position_fingerprint('entreatment'))
        '0b101011111111'

        """
        position = {}
        for pos, letter in enumerate(word):
            if letter not in position and letter in most_common:
                position[letter] = min(pos, 2 ** bits_per_letter - 1)

        fingerprint = 0

        for letter in most_common:
            if n_bits:
                fingerprint <<= min(bits_per_letter, n_bits)
                if letter in position:
                    fingerprint += min(position[letter], 2 ** n_bits - 1)
                else:
                    fingerprint += min(
                        2 ** bits_per_letter - 1, 2 ** n_bits - 1
                    )
                n_bits -= min(bits_per_letter, n_bits)
            else:
                break

        for _ in range(n_bits):
            fingerprint <<= 1
            fingerprint += 1

        return fingerprint