def encode(self, word, max_length=-1, zero_pad=False, retain_vowels=False):
        """Return the Refined Soundex code for a word.

        Parameters
        ----------
        word : str
            The word to transform
        max_length : int
            The length of the code returned (defaults to unlimited)
        zero_pad : bool
            Pad the end of the return value with 0s to achieve a max_length
            string
        retain_vowels : bool
            Retain vowels (as 0) in the resulting code

        Returns
        -------
        str
            The Refined Soundex value

        Examples
        --------
        >>> pe = RefinedSoundex()
        >>> pe.encode('Christopher')
        'C393619'
        >>> pe.encode('Niall')
        'N87'
        >>> pe.encode('Smith')
        'S386'
        >>> pe.encode('Schmidt')
        'S386'

        """
        # uppercase, normalize, decompose, and filter non-A-Z out
        word = unicode_normalize('NFKD', text_type(word.upper()))
        word = word.replace('ß', 'SS')
        word = ''.join(c for c in word if c in self._uc_set)

        # apply the Soundex algorithm
        sdx = word[:1] + word.translate(self._trans)
        sdx = self._delete_consecutive_repeats(sdx)
        if not retain_vowels:
            sdx = sdx.replace('0', '')  # Delete vowels, H, W, Y

        if max_length > 0:
            if zero_pad:
                sdx += '0' * max_length
            sdx = sdx[:max_length]

        return sdx