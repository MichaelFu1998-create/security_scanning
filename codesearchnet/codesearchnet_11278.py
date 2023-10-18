def encode(self, word):
        """Return the Phonem code for a word.

        Parameters
        ----------
        word : str
        The word to transform

        Returns
        -------
        str
            The Phonem value

        Examples
        --------
        >>> pe = Phonem()
        >>> pe.encode('Christopher')
        'CRYSDOVR'
        >>> pe.encode('Niall')
        'NYAL'
        >>> pe.encode('Smith')
        'SMYD'
        >>> pe.encode('Schmidt')
        'CMYD'

        """
        word = unicode_normalize('NFC', text_type(word.upper()))
        for i, j in self._substitutions:
            word = word.replace(i, j)
        word = word.translate(self._trans)

        return ''.join(
            c
            for c in self._delete_consecutive_repeats(word)
            if c in self._uc_set
        )