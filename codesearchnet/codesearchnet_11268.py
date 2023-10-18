def fingerprint(self, word, n_bits=16, most_common=MOST_COMMON_LETTERS_CG):
        """Return the occurrence halved fingerprint.

        Based on the occurrence halved fingerprint from :cite:`Cislak:2017`.

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
            The occurrence halved fingerprint

        Examples
        --------
        >>> ohf = OccurrenceHalved()
        >>> bin(ohf.fingerprint('hat'))
        '0b1010000000010'
        >>> bin(ohf.fingerprint('niall'))
        '0b10010100000'
        >>> bin(ohf.fingerprint('colin'))
        '0b1001010000'
        >>> bin(ohf.fingerprint('atcg'))
        '0b10100000000000'
        >>> bin(ohf.fingerprint('entreatment'))
        '0b1111010000110000'

        """
        if n_bits % 2:
            n_bits += 1

        w_len = len(word) // 2
        w_1 = set(word[:w_len])
        w_2 = set(word[w_len:])
        fingerprint = 0

        for letter in most_common:
            if n_bits:
                fingerprint <<= 1
                if letter in w_1:
                    fingerprint += 1
                fingerprint <<= 1
                if letter in w_2:
                    fingerprint += 1
                n_bits -= 2
            else:
                break

        if n_bits > 0:
            fingerprint <<= n_bits

        return fingerprint