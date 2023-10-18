def stem(self, word):
        """Return CLEF Swedish stem.

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
        >>> clef_swedish('undervisa')
        'undervis'
        >>> clef_swedish('suspension')
        'suspensio'
        >>> clef_swedish('visshet')
        'viss'

        """
        wlen = len(word) - 2

        if wlen > 2 and word[-1] == 's':
            word = word[:-1]
            wlen -= 1

        _endings = {
            5: {'elser', 'heten'},
            4: {'arne', 'erna', 'ande', 'else', 'aste', 'orna', 'aren'},
            3: {'are', 'ast', 'het'},
            2: {'ar', 'er', 'or', 'en', 'at', 'te', 'et'},
            1: {'a', 'e', 'n', 't'},
        }

        for end_len in range(5, 0, -1):
            if wlen > end_len and word[-end_len:] in _endings[end_len]:
                return word[:-end_len]
        return word