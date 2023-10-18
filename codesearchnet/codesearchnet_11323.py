def _synoname_strip_punct(self, word):
        """Return a word with punctuation stripped out.

        Parameters
        ----------
        word : str
            A word to strip punctuation from

        Returns
        -------
        str
            The word stripped of punctuation

        Examples
        --------
        >>> pe = Synoname()
        >>> pe._synoname_strip_punct('AB;CD EF-GH$IJ')
        'ABCD EFGHIJ'

        """
        stripped = ''
        for char in word:
            if char not in set(',-./:;"&\'()!{|}?$%*+<=>[\\]^_`~'):
                stripped += char
        return stripped.strip()