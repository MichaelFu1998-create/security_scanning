def encode(self, word):
        """Return Reth-Schek Phonetik code for a word.

        Parameters
        ----------
        word : str
            The word to transform

        Returns
        -------
        str
            The Reth-Schek Phonetik code

        Examples
        --------
        >>> reth_schek_phonetik('Joachim')
        'JOAGHIM'
        >>> reth_schek_phonetik('Christoph')
        'GHRISDOF'
        >>> reth_schek_phonetik('Jörg')
        'JOERG'
        >>> reth_schek_phonetik('Smith')
        'SMID'
        >>> reth_schek_phonetik('Schmidt')
        'SCHMID'

        """
        # Uppercase
        word = word.upper()

        # Replace umlauts/eszett
        word = word.replace('Ä', 'AE')
        word = word.replace('Ö', 'OE')
        word = word.replace('Ü', 'UE')
        word = word.replace('ß', 'SS')

        # Main loop, using above replacements table
        pos = 0
        while pos < len(word):
            for num in range(3, 0, -1):
                if word[pos : pos + num] in self._replacements[num]:
                    word = (
                        word[:pos]
                        + self._replacements[num][word[pos : pos + num]]
                        + word[pos + num :]
                    )
                    pos += 1
                    break
            else:
                pos += 1  # Advance if nothing is recognized

        # Change 'CH' back(?) to 'SCH'
        word = word.replace('CH', 'SCH')

        # Replace final sequences
        if word[-2:] == 'ER':
            word = word[:-2] + 'R'
        elif word[-2:] == 'EL':
            word = word[:-2] + 'L'
        elif word[-1:] == 'H':
            word = word[:-1]

        return word