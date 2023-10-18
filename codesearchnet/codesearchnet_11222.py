def fingerprint(self, word):
        """Return the skeleton key.

        Parameters
        ----------
        word : str
            The word to transform into its skeleton key

        Returns
        -------
        str
            The skeleton key

        Examples
        --------
        >>> sk = SkeletonKey()
        >>> sk.fingerprint('The quick brown fox jumped over the lazy dog.')
        'THQCKBRWNFXJMPDVLZYGEUIOA'
        >>> sk.fingerprint('Christopher')
        'CHRSTPIOE'
        >>> sk.fingerprint('Niall')
        'NLIA'

        """
        word = unicode_normalize('NFKD', text_type(word.upper()))
        word = ''.join(c for c in word if c in self._letters)
        start = word[0:1]
        consonant_part = ''
        vowel_part = ''

        # add consonants & vowels to to separate strings
        # (omitting the first char & duplicates)
        for char in word[1:]:
            if char != start:
                if char in self._vowels:
                    if char not in vowel_part:
                        vowel_part += char
                elif char not in consonant_part:
                    consonant_part += char
        # return the first char followed by consonants followed by vowels
        return start + consonant_part + vowel_part