def encode(self, word, max_length=4):
        """Return the Statistics Canada code for a word.

        Parameters
        ----------
        word : str
            The word to transform
        max_length : int
            The maximum length (default 4) of the code to return

        Returns
        -------
        str
            The Statistics Canada name code value

        Examples
        --------
        >>> pe = StatisticsCanada()
        >>> pe.encode('Christopher')
        'CHRS'
        >>> pe.encode('Niall')
        'NL'
        >>> pe.encode('Smith')
        'SMTH'
        >>> pe.encode('Schmidt')
        'SCHM'

        """
        # uppercase, normalize, decompose, and filter non-A-Z out
        word = unicode_normalize('NFKD', text_type(word.upper()))
        word = word.replace('ß', 'SS')
        word = ''.join(c for c in word if c in self._uc_set)
        if not word:
            return ''

        code = word[1:]
        for vowel in self._uc_vy_set:
            code = code.replace(vowel, '')
        code = word[0] + code
        code = self._delete_consecutive_repeats(code)
        code = code.replace(' ', '')

        return code[:max_length]