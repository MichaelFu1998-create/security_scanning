def encode(self, word, max_length=5, zero_pad=True):
        """Return the Roger Root code for a word.

        Parameters
        ----------
        word : str
            The word to transform
        max_length : int
            The maximum length (default 5) of the code to return
        zero_pad : bool
            Pad the end of the return value with 0s to achieve a max_length
            string

        Returns
        -------
        str
            The Roger Root code

        Examples
        --------
        >>> roger_root('Christopher')
        '06401'
        >>> roger_root('Niall')
        '02500'
        >>> roger_root('Smith')
        '00310'
        >>> roger_root('Schmidt')
        '06310'

        """
        # uppercase, normalize, decompose, and filter non-A-Z out
        word = unicode_normalize('NFKD', text_type(word.upper()))
        word = word.replace('ß', 'SS')
        word = ''.join(c for c in word if c in self._uc_set)

        code = ''
        pos = 0

        # Do first digit(s) first
        for num in range(4, 0, -1):
            if word[:num] in self._init_patterns[num]:
                code = self._init_patterns[num][word[:num]]
                pos += num
                break

        # Then code subsequent digits
        while pos < len(word):
            for num in range(4, 0, -1):  # pragma: no branch
                if word[pos : pos + num] in self._med_patterns[num]:
                    code += self._med_patterns[num][word[pos : pos + num]]
                    pos += num
                    break

        code = self._delete_consecutive_repeats(code)
        code = code.replace('*', '')

        if zero_pad:
            code += '0' * max_length

        return code[:max_length]