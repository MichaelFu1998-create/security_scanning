def stem(self, word, alternate_vowels=False):
        """Return Snowball German stem.

        Parameters
        ----------
        word : str
            The word to stem
        alternate_vowels : bool
            Composes ae as ה, oe as צ, and ue as ü before running the algorithm

        Returns
        -------
        str
            Word stem

        Examples
        --------
        >>> stmr = SnowballGerman()
        >>> stmr.stem('lesen')
        'les'
        >>> stmr.stem('graues')
        'grau'
        >>> stmr.stem('buchstabieren')
        'buchstabi'

        """
        # lowercase, normalize, and compose
        word = normalize('NFC', word.lower())
        word = word.replace('ß', 'ss')

        if len(word) > 2:
            for i in range(2, len(word)):
                if word[i] in self._vowels and word[i - 2] in self._vowels:
                    if word[i - 1] == 'u':
                        word = word[: i - 1] + 'U' + word[i:]
                    elif word[i - 1] == 'y':
                        word = word[: i - 1] + 'Y' + word[i:]

        if alternate_vowels:
            word = word.replace('ae', 'ה')
            word = word.replace('oe', 'צ')
            word = word.replace('que', 'Q')
            word = word.replace('ue', 'ü')
            word = word.replace('Q', 'que')

        r1_start = max(3, self._sb_r1(word))
        r2_start = self._sb_r2(word)

        # Step 1
        niss_flag = False
        if word[-3:] == 'ern':
            if len(word[r1_start:]) >= 3:
                word = word[:-3]
        elif word[-2:] == 'em':
            if len(word[r1_start:]) >= 2:
                word = word[:-2]
        elif word[-2:] == 'er':
            if len(word[r1_start:]) >= 2:
                word = word[:-2]
        elif word[-2:] == 'en':
            if len(word[r1_start:]) >= 2:
                word = word[:-2]
                niss_flag = True
        elif word[-2:] == 'es':
            if len(word[r1_start:]) >= 2:
                word = word[:-2]
                niss_flag = True
        elif word[-1:] == 'e':
            if len(word[r1_start:]) >= 1:
                word = word[:-1]
                niss_flag = True
        elif word[-1:] == 's':
            if (
                len(word[r1_start:]) >= 1
                and len(word) >= 2
                and word[-2] in self._s_endings
            ):
                word = word[:-1]

        if niss_flag and word[-4:] == 'niss':
            word = word[:-1]

        # Step 2
        if word[-3:] == 'est':
            if len(word[r1_start:]) >= 3:
                word = word[:-3]
        elif word[-2:] == 'en':
            if len(word[r1_start:]) >= 2:
                word = word[:-2]
        elif word[-2:] == 'er':
            if len(word[r1_start:]) >= 2:
                word = word[:-2]
        elif word[-2:] == 'st':
            if (
                len(word[r1_start:]) >= 2
                and len(word) >= 6
                and word[-3] in self._st_endings
            ):
                word = word[:-2]

        # Step 3
        if word[-4:] == 'isch':
            if len(word[r2_start:]) >= 4 and word[-5] != 'e':
                word = word[:-4]
        elif word[-4:] in {'lich', 'heit'}:
            if len(word[r2_start:]) >= 4:
                word = word[:-4]
                if word[-2:] in {'er', 'en'} and len(word[r1_start:]) >= 2:
                    word = word[:-2]
        elif word[-4:] == 'keit':
            if len(word[r2_start:]) >= 4:
                word = word[:-4]
                if word[-4:] == 'lich' and len(word[r2_start:]) >= 4:
                    word = word[:-4]
                elif word[-2:] == 'ig' and len(word[r2_start:]) >= 2:
                    word = word[:-2]
        elif word[-3:] in {'end', 'ung'}:
            if len(word[r2_start:]) >= 3:
                word = word[:-3]
                if (
                    word[-2:] == 'ig'
                    and len(word[r2_start:]) >= 2
                    and word[-3] != 'e'
                ):
                    word = word[:-2]
        elif word[-2:] in {'ig', 'ik'}:
            if len(word[r2_start:]) >= 2 and word[-3] != 'e':
                word = word[:-2]

        # Change 'Y' and 'U' back to lowercase if survived stemming
        for i in range(0, len(word)):
            if word[i] == 'Y':
                word = word[:i] + 'y' + word[i + 1 :]
            elif word[i] == 'U':
                word = word[:i] + 'u' + word[i + 1 :]

        # Remove umlauts
        _umlauts = dict(zip((ord(_) for _ in 'הצü'), 'aou'))
        word = word.translate(_umlauts)

        return word