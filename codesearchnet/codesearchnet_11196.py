def stem(self, word):
        """Return CLEF German stem.

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
        >>> stmr = CLEFGerman()
        >>> stmr.stem('lesen')
        'lese'
        >>> stmr.stem('graues')
        'grau'
        >>> stmr.stem('buchstabieren')
        'buchstabier'

        """
        # lowercase, normalize, and compose
        word = normalize('NFC', text_type(word.lower()))

        # remove umlauts
        word = word.translate(self._umlauts)

        # remove plurals
        wlen = len(word) - 1

        if wlen > 3:
            if wlen > 5:
                if word[-3:] == 'nen':
                    return word[:-3]
            if wlen > 4:
                if word[-2:] in {'en', 'se', 'es', 'er'}:
                    return word[:-2]
            if word[-1] in {'e', 'n', 'r', 's'}:
                return word[:-1]
        return word