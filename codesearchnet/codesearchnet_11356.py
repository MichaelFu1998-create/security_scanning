def stem(self, word):
        """Return Lovins stem.

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
        >>> stmr = Lovins()
        >>> stmr.stem('reading')
        'read'
        >>> stmr.stem('suspension')
        'suspens'
        >>> stmr.stem('elusiveness')
        'elus'

        """
        # lowercase, normalize, and compose
        word = normalize('NFC', text_type(word.lower()))

        for suffix_len in range(11, 0, -1):
            ending = word[-suffix_len:]
            if (
                ending in self._suffix
                and len(word) - suffix_len >= 2
                and (
                    self._suffix[ending] is None
                    or self._suffix[ending](word, suffix_len)
                )
            ):
                word = word[:-suffix_len]
                break

        if word[-2:] in {
            'bb',
            'dd',
            'gg',
            'll',
            'mm',
            'nn',
            'pp',
            'rr',
            'ss',
            'tt',
        }:
            word = word[:-1]

        for ending, replacement in self._recode:
            if word.endswith(ending):
                if callable(replacement):
                    word = replacement(word)
                else:
                    word = word[: -len(ending)] + replacement

        return word