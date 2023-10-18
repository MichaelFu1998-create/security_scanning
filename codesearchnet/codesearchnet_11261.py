def fingerprint(self, word):
        """Return the omission key.

        Parameters
        ----------
        word : str
            The word to transform into its omission key

        Returns
        -------
        str
            The omission key

        Examples
        --------
        >>> ok = OmissionKey()
        >>> ok.fingerprint('The quick brown fox jumped over the lazy dog.')
        'JKQXZVWYBFMGPDHCLNTREUIOA'
        >>> ok.fingerprint('Christopher')
        'PHCTSRIOE'
        >>> ok.fingerprint('Niall')
        'LNIA'

        """
        word = unicode_normalize('NFKD', text_type(word.upper()))
        word = ''.join(c for c in word if c in self._letters)

        key = ''

        # add consonants in order supplied by _consonants (no duplicates)
        for char in self._consonants:
            if char in word:
                key += char

        # add vowels in order they appeared in the word (no duplicates)
        for char in word:
            if char not in self._consonants and char not in key:
                key += char

        return key