def stem(self, word):
        """Return the S-stemmed form of a word.

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
        >>> stmr = SStemmer()
        >>> stmr.stem('summaries')
        'summary'
        >>> stmr.stem('summary')
        'summary'
        >>> stmr.stem('towers')
        'tower'
        >>> stmr.stem('reading')
        'reading'
        >>> stmr.stem('census')
        'census'

        """
        lowered = word.lower()
        if lowered[-3:] == 'ies' and lowered[-4:-3] not in {'e', 'a'}:
            return word[:-3] + ('Y' if word[-1:].isupper() else 'y')
        if lowered[-2:] == 'es' and lowered[-3:-2] not in {'a', 'e', 'o'}:
            return word[:-1]
        if lowered[-1:] == 's' and lowered[-2:-1] not in {'u', 's'}:
            return word[:-1]
        return word