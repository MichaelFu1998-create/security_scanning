def encode(self, word):
        """Return the MRA personal numeric identifier (PNI) for a word.

        Parameters
        ----------
        word : str
            The word to transform

        Returns
        -------
        str
            The MRA PNI

        Examples
        --------
        >>> pe = MRA()
        >>> pe.encode('Christopher')
        'CHRPHR'
        >>> pe.encode('Niall')
        'NL'
        >>> pe.encode('Smith')
        'SMTH'
        >>> pe.encode('Schmidt')
        'SCHMDT'

        """
        if not word:
            return word
        word = word.upper()
        word = word.replace('ß', 'SS')
        word = word[0] + ''.join(
            c for c in word[1:] if c not in self._uc_v_set
        )
        word = self._delete_consecutive_repeats(word)
        if len(word) > 6:
            word = word[:3] + word[-3:]
        return word