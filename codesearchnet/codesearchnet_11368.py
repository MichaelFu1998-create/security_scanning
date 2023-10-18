def stem(self, word):
        """Return 'CLEF German stemmer plus' stem.

        Parameters
        ----------
        word : str
            The word to stem

        Returns
        -------
        str
            Word stem

        Examples
        --------
        >>> stmr = CLEFGermanPlus()
        >>> clef_german_plus('lesen')
        'les'
        >>> clef_german_plus('graues')
        'grau'
        >>> clef_german_plus('buchstabieren')
        'buchstabi'

        """
        # lowercase, normalize, and compose
        word = normalize('NFC', text_type(word.lower()))

        # remove umlauts
        word = word.translate(self._accents)

        # Step 1
        wlen = len(word) - 1
        if wlen > 4 and word[-3:] == 'ern':
            word = word[:-3]
        elif wlen > 3 and word[-2:] in {'em', 'en', 'er', 'es'}:
            word = word[:-2]
        elif wlen > 2 and (
            word[-1] == 'e'
            or (word[-1] == 's' and word[-2] in self._st_ending)
        ):
            word = word[:-1]

        # Step 2
        wlen = len(word) - 1
        if wlen > 4 and word[-3:] == 'est':
            word = word[:-3]
        elif wlen > 3 and (
            word[-2:] in {'er', 'en'}
            or (word[-2:] == 'st' and word[-3] in self._st_ending)
        ):
            word = word[:-2]

        return word