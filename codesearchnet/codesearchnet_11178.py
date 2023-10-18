def encode(self, word):
        """Return the Norphone code.

        Parameters
        ----------
        word : str
            The word to transform

        Returns
        -------
        str
            The Norphone code

        Examples
        --------
        >>> pe = Norphone()
        >>> pe.encode('Hansen')
        'HNSN'
        >>> pe.encode('Larsen')
        'LRSN'
        >>> pe.encode('Aagaard')
        'ÅKRT'
        >>> pe.encode('Braaten')
        'BRTN'
        >>> pe.encode('Sandvik')
        'SNVK'

        """
        word = word.upper()

        code = ''
        skip = 0

        if word[0:2] == 'AA':
            code = 'Å'
            skip = 2
        elif word[0:2] == 'GI':
            code = 'J'
            skip = 2
        elif word[0:3] == 'SKY':
            code = 'X'
            skip = 3
        elif word[0:2] == 'EI':
            code = 'Æ'
            skip = 2
        elif word[0:2] == 'KY':
            code = 'X'
            skip = 2
        elif word[:1] == 'C':
            code = 'K'
            skip = 1
        elif word[:1] == 'Ä':
            code = 'Æ'
            skip = 1
        elif word[:1] == 'Ö':
            code = 'Ø'
            skip = 1

        if word[-2:] == 'DT':
            word = word[:-2] + 'T'
        # Though the rules indicate this rule applies in all positions, the
        # reference implementation indicates it applies only in final position.
        elif word[-2:-1] in self._uc_v_set and word[-1:] == 'D':
            word = word[:-2]

        for pos, char in enumerate(word):
            if skip:
                skip -= 1
            else:
                for length in sorted(self._replacements, reverse=True):
                    if word[pos : pos + length] in self._replacements[length]:
                        code += self._replacements[length][
                            word[pos : pos + length]
                        ]
                        skip = length - 1
                        break
                else:
                    if not pos or char not in self._uc_v_set:
                        code += char

        code = self._delete_consecutive_repeats(code)

        return code