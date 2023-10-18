def encode(self, word):
        """Return the Standardized Phonetic Frequency Code (SPFC) of a word.

        Parameters
        ----------
        word : str
            The word to transform

        Returns
        -------
        str
            The SPFC value

        Raises
        ------
        AttributeError
            Word attribute must be a string with a space or period dividing the
            first and last names or a tuple/list consisting of the first and
            last names

        Examples
        --------
        >>> pe = SPFC()
        >>> pe.encode('Christopher Smith')
        '01160'
        >>> pe.encode('Christopher Schmidt')
        '01160'
        >>> pe.encode('Niall Smith')
        '01660'
        >>> pe.encode('Niall Schmidt')
        '01660'

        >>> pe.encode('L.Smith')
        '01960'
        >>> pe.encode('R.Miller')
        '65490'

        >>> pe.encode(('L', 'Smith'))
        '01960'
        >>> pe.encode(('R', 'Miller'))
        '65490'

        """

        def _raise_word_ex():
            """Raise an AttributeError.

            Raises
            ------
            AttributeError
                Word attribute must be a string with a space or period dividing
                the first and last names or a tuple/list consisting of the
                first and last names

            """
            raise AttributeError(
                'Word attribute must be a string with a space or period '
                + 'dividing the first and last names or a tuple/list '
                + 'consisting of the first and last names'
            )

        if not word:
            return ''

        names = []
        if isinstance(word, (str, text_type)):
            names = word.split('.', 1)
            if len(names) != 2:
                names = word.split(' ', 1)
                if len(names) != 2:
                    _raise_word_ex()
        elif hasattr(word, '__iter__'):
            if len(word) != 2:
                _raise_word_ex()
            names = word
        else:
            _raise_word_ex()

        names = [
            unicode_normalize(
                'NFKD', text_type(_.strip().replace('ß', 'SS').upper())
            )
            for _ in names
        ]
        code = ''

        def _steps_one_to_three(name):
            """Perform the first three steps of SPFC.

            Parameters
            ----------
            name : str
                Name to transform

            Returns
            -------
            str
                Transformed name

            """
            # filter out non A-Z
            name = ''.join(_ for _ in name if _ in self._uc_set)

            # 1. In the field, convert DK to K, DT to T, SC to S, KN to N,
            # and MN to N
            for subst in self._substitutions:
                name = name.replace(subst[0], subst[1])

            # 2. In the name field, replace multiple letters with a single
            # letter
            name = self._delete_consecutive_repeats(name)

            # 3. Remove vowels, W, H, and Y, but keep the first letter in the
            # name field.
            if name:
                name = name[0] + ''.join(
                    _
                    for _ in name[1:]
                    if _ not in {'A', 'E', 'H', 'I', 'O', 'U', 'W', 'Y'}
                )
            return name

        names = [_steps_one_to_three(_) for _ in names]

        # 4. The first digit of the code is obtained using PF1 and the first
        # letter of the name field. Remove this letter after coding.
        if names[1]:
            code += names[1][0].translate(self._pf1)
            names[1] = names[1][1:]

        # 5. Using the last letters of the name, use Table PF3 to obtain the
        # second digit of the code. Use as many letters as possible and remove
        # after coding.
        if names[1]:
            if names[1][-3:] == 'STN' or names[1][-3:] == 'PRS':
                code += '8'
                names[1] = names[1][:-3]
            elif names[1][-2:] == 'SN':
                code += '8'
                names[1] = names[1][:-2]
            elif names[1][-3:] == 'STR':
                code += '9'
                names[1] = names[1][:-3]
            elif names[1][-2:] in {'SR', 'TN', 'TD'}:
                code += '9'
                names[1] = names[1][:-2]
            elif names[1][-3:] == 'DRS':
                code += '7'
                names[1] = names[1][:-3]
            elif names[1][-2:] in {'TR', 'MN'}:
                code += '7'
                names[1] = names[1][:-2]
            else:
                code += names[1][-1].translate(self._pf3)
                names[1] = names[1][:-1]

        # 6. The third digit is found using Table PF2 and the first character
        # of the first name. Remove after coding.
        if names[0]:
            code += names[0][0].translate(self._pf2)
            names[0] = names[0][1:]

        # 7. The fourth digit is found using Table PF2 and the first character
        # of the name field. If no letters remain use zero. After coding remove
        # the letter.
        # 8. The fifth digit is found in the same manner as the fourth using
        # the remaining characters of the name field if any.
        for _ in range(2):
            if names[1]:
                code += names[1][0].translate(self._pf2)
                names[1] = names[1][1:]
            else:
                code += '0'

        return code