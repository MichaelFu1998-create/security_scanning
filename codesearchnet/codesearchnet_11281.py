def stem(self, word):
        """Return Snowball Dutch stem.

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
        >>> stmr = SnowballDutch()
        >>> stmr.stem('lezen')
        'lez'
        >>> stmr.stem('opschorting')
        'opschort'
        >>> stmr.stem('ongrijpbaarheid')
        'ongrijp'

        """
        # lowercase, normalize, decompose, filter umlauts & acutes out, and
        # compose
        word = normalize('NFC', text_type(word.lower()))
        word = word.translate(self._accented)

        for i in range(len(word)):
            if i == 0 and word[0] == 'y':
                word = 'Y' + word[1:]
            elif word[i] == 'y' and word[i - 1] in self._vowels:
                word = word[:i] + 'Y' + word[i + 1 :]
            elif (
                word[i] == 'i'
                and word[i - 1] in self._vowels
                and i + 1 < len(word)
                and word[i + 1] in self._vowels
            ):
                word = word[:i] + 'I' + word[i + 1 :]

        r1_start = max(3, self._sb_r1(word))
        r2_start = self._sb_r2(word)

        # Step 1
        if word[-5:] == 'heden':
            if len(word[r1_start:]) >= 5:
                word = word[:-3] + 'id'
        elif word[-3:] == 'ene':
            if len(word[r1_start:]) >= 3 and (
                word[-4] not in self._vowels and word[-6:-3] != 'gem'
            ):
                word = self._undouble(word[:-3])
        elif word[-2:] == 'en':
            if len(word[r1_start:]) >= 2 and (
                word[-3] not in self._vowels and word[-5:-2] != 'gem'
            ):
                word = self._undouble(word[:-2])
        elif word[-2:] == 'se':
            if (
                len(word[r1_start:]) >= 2
                and word[-3] not in self._not_s_endings
            ):
                word = word[:-2]
        elif word[-1:] == 's':
            if (
                len(word[r1_start:]) >= 1
                and word[-2] not in self._not_s_endings
            ):
                word = word[:-1]

        # Step 2
        e_removed = False
        if word[-1:] == 'e':
            if len(word[r1_start:]) >= 1 and word[-2] not in self._vowels:
                word = self._undouble(word[:-1])
                e_removed = True

        # Step 3a
        if word[-4:] == 'heid':
            if len(word[r2_start:]) >= 4 and word[-5] != 'c':
                word = word[:-4]
                if word[-2:] == 'en':
                    if len(word[r1_start:]) >= 2 and (
                        word[-3] not in self._vowels and word[-5:-2] != 'gem'
                    ):
                        word = self._undouble(word[:-2])

        # Step 3b
        if word[-4:] == 'lijk':
            if len(word[r2_start:]) >= 4:
                word = word[:-4]
                # Repeat step 2
                if word[-1:] == 'e':
                    if (
                        len(word[r1_start:]) >= 1
                        and word[-2] not in self._vowels
                    ):
                        word = self._undouble(word[:-1])
        elif word[-4:] == 'baar':
            if len(word[r2_start:]) >= 4:
                word = word[:-4]
        elif word[-3:] in ('end', 'ing'):
            if len(word[r2_start:]) >= 3:
                word = word[:-3]
                if (
                    word[-2:] == 'ig'
                    and len(word[r2_start:]) >= 2
                    and word[-3] != 'e'
                ):
                    word = word[:-2]
                else:
                    word = self._undouble(word)
        elif word[-3:] == 'bar':
            if len(word[r2_start:]) >= 3 and e_removed:
                word = word[:-3]
        elif word[-2:] == 'ig':
            if len(word[r2_start:]) >= 2 and word[-3] != 'e':
                word = word[:-2]

        # Step 4
        if (
            len(word) >= 4
            and word[-3] == word[-2]
            and word[-2] in {'a', 'e', 'o', 'u'}
            and word[-4] not in self._vowels
            and word[-1] not in self._vowels
            and word[-1] != 'I'
        ):
            word = word[:-2] + word[-1]

        # Change 'Y' and 'U' back to lowercase if survived stemming
        for i in range(0, len(word)):
            if word[i] == 'Y':
                word = word[:i] + 'y' + word[i + 1 :]
            elif word[i] == 'I':
                word = word[:i] + 'i' + word[i + 1 :]

        return word