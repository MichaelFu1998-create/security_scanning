def stem(self, word, early_english=False):
        """Return the Porter2 (Snowball English) stem.

        Parameters
        ----------
        word : str
            The word to stem
        early_english : bool
            Set to True in order to remove -eth & -est (2nd & 3rd person
            singular verbal agreement suffixes)

        Returns
        -------
        str
            Word stem

        Examples
        --------
        >>> stmr = Porter2()
        >>> stmr.stem('reading')
        'read'
        >>> stmr.stem('suspension')
        'suspens'
        >>> stmr.stem('elusiveness')
        'elus'

        >>> stmr.stem('eateth', early_english=True)
        'eat'

        """
        # lowercase, normalize, and compose
        word = normalize('NFC', text_type(word.lower()))
        # replace apostrophe-like characters with U+0027, per
        # http://snowball.tartarus.org/texts/apostrophe.html
        word = word.replace('’', '\'')
        word = word.replace('’', '\'')

        # Exceptions 1
        if word in self._exception1dict:
            return self._exception1dict[word]
        elif word in self._exception1set:
            return word

        # Return word if stem is shorter than 3
        if len(word) < 3:
            return word

        # Remove initial ', if present.
        while word and word[0] == '\'':
            word = word[1:]
            # Return word if stem is shorter than 2
            if len(word) < 2:
                return word

        # Re-map vocalic Y to y (Y will be C, y will be V)
        if word[0] == 'y':
            word = 'Y' + word[1:]
        for i in range(1, len(word)):
            if word[i] == 'y' and word[i - 1] in self._vowels:
                word = word[:i] + 'Y' + word[i + 1 :]

        r1_start = self._sb_r1(word, self._r1_prefixes)
        r2_start = self._sb_r2(word, self._r1_prefixes)

        # Step 0
        if word[-3:] == '\'s\'':
            word = word[:-3]
        elif word[-2:] == '\'s':
            word = word[:-2]
        elif word[-1:] == '\'':
            word = word[:-1]
        # Return word if stem is shorter than 2
        if len(word) < 3:
            return word

        # Step 1a
        if word[-4:] == 'sses':
            word = word[:-2]
        elif word[-3:] in {'ied', 'ies'}:
            if len(word) > 4:
                word = word[:-2]
            else:
                word = word[:-1]
        elif word[-2:] in {'us', 'ss'}:
            pass
        elif word[-1] == 's':
            if self._sb_has_vowel(word[:-2]):
                word = word[:-1]

        # Exceptions 2
        if word in self._exception2set:
            return word

        # Step 1b
        step1b_flag = False
        if word[-5:] == 'eedly':
            if len(word[r1_start:]) >= 5:
                word = word[:-3]
        elif word[-5:] == 'ingly':
            if self._sb_has_vowel(word[:-5]):
                word = word[:-5]
                step1b_flag = True
        elif word[-4:] == 'edly':
            if self._sb_has_vowel(word[:-4]):
                word = word[:-4]
                step1b_flag = True
        elif word[-3:] == 'eed':
            if len(word[r1_start:]) >= 3:
                word = word[:-1]
        elif word[-3:] == 'ing':
            if self._sb_has_vowel(word[:-3]):
                word = word[:-3]
                step1b_flag = True
        elif word[-2:] == 'ed':
            if self._sb_has_vowel(word[:-2]):
                word = word[:-2]
                step1b_flag = True
        elif early_english:
            if word[-3:] == 'est':
                if self._sb_has_vowel(word[:-3]):
                    word = word[:-3]
                    step1b_flag = True
            elif word[-3:] == 'eth':
                if self._sb_has_vowel(word[:-3]):
                    word = word[:-3]
                    step1b_flag = True

        if step1b_flag:
            if word[-2:] in {'at', 'bl', 'iz'}:
                word += 'e'
            elif word[-2:] in self._doubles:
                word = word[:-1]
            elif self._sb_short_word(word, self._r1_prefixes):
                word += 'e'

        # Step 1c
        if (
            len(word) > 2
            and word[-1] in {'Y', 'y'}
            and word[-2] not in self._vowels
        ):
            word = word[:-1] + 'i'

        # Step 2
        if word[-2] == 'a':
            if word[-7:] == 'ational':
                if len(word[r1_start:]) >= 7:
                    word = word[:-5] + 'e'
            elif word[-6:] == 'tional':
                if len(word[r1_start:]) >= 6:
                    word = word[:-2]
        elif word[-2] == 'c':
            if word[-4:] in {'enci', 'anci'}:
                if len(word[r1_start:]) >= 4:
                    word = word[:-1] + 'e'
        elif word[-2] == 'e':
            if word[-4:] == 'izer':
                if len(word[r1_start:]) >= 4:
                    word = word[:-1]
        elif word[-2] == 'g':
            if word[-3:] == 'ogi':
                if (
                    r1_start >= 1
                    and len(word[r1_start:]) >= 3
                    and word[-4] == 'l'
                ):
                    word = word[:-1]
        elif word[-2] == 'l':
            if word[-6:] == 'lessli':
                if len(word[r1_start:]) >= 6:
                    word = word[:-2]
            elif word[-5:] in {'entli', 'fulli', 'ousli'}:
                if len(word[r1_start:]) >= 5:
                    word = word[:-2]
            elif word[-4:] == 'abli':
                if len(word[r1_start:]) >= 4:
                    word = word[:-1] + 'e'
            elif word[-4:] == 'alli':
                if len(word[r1_start:]) >= 4:
                    word = word[:-2]
            elif word[-3:] == 'bli':
                if len(word[r1_start:]) >= 3:
                    word = word[:-1] + 'e'
            elif word[-2:] == 'li':
                if (
                    r1_start >= 1
                    and len(word[r1_start:]) >= 2
                    and word[-3] in self._li
                ):
                    word = word[:-2]
        elif word[-2] == 'o':
            if word[-7:] == 'ization':
                if len(word[r1_start:]) >= 7:
                    word = word[:-5] + 'e'
            elif word[-5:] == 'ation':
                if len(word[r1_start:]) >= 5:
                    word = word[:-3] + 'e'
            elif word[-4:] == 'ator':
                if len(word[r1_start:]) >= 4:
                    word = word[:-2] + 'e'
        elif word[-2] == 's':
            if word[-7:] in {'fulness', 'ousness', 'iveness'}:
                if len(word[r1_start:]) >= 7:
                    word = word[:-4]
            elif word[-5:] == 'alism':
                if len(word[r1_start:]) >= 5:
                    word = word[:-3]
        elif word[-2] == 't':
            if word[-6:] == 'biliti':
                if len(word[r1_start:]) >= 6:
                    word = word[:-5] + 'le'
            elif word[-5:] == 'aliti':
                if len(word[r1_start:]) >= 5:
                    word = word[:-3]
            elif word[-5:] == 'iviti':
                if len(word[r1_start:]) >= 5:
                    word = word[:-3] + 'e'

        # Step 3
        if word[-7:] == 'ational':
            if len(word[r1_start:]) >= 7:
                word = word[:-5] + 'e'
        elif word[-6:] == 'tional':
            if len(word[r1_start:]) >= 6:
                word = word[:-2]
        elif word[-5:] in {'alize', 'icate', 'iciti'}:
            if len(word[r1_start:]) >= 5:
                word = word[:-3]
        elif word[-5:] == 'ative':
            if len(word[r2_start:]) >= 5:
                word = word[:-5]
        elif word[-4:] == 'ical':
            if len(word[r1_start:]) >= 4:
                word = word[:-2]
        elif word[-4:] == 'ness':
            if len(word[r1_start:]) >= 4:
                word = word[:-4]
        elif word[-3:] == 'ful':
            if len(word[r1_start:]) >= 3:
                word = word[:-3]

        # Step 4
        for suffix in (
            'ement',
            'ance',
            'ence',
            'able',
            'ible',
            'ment',
            'ant',
            'ent',
            'ism',
            'ate',
            'iti',
            'ous',
            'ive',
            'ize',
            'al',
            'er',
            'ic',
        ):
            if word[-len(suffix) :] == suffix:
                if len(word[r2_start:]) >= len(suffix):
                    word = word[: -len(suffix)]
                break
        else:
            if word[-3:] == 'ion':
                if (
                    len(word[r2_start:]) >= 3
                    and len(word) >= 4
                    and word[-4] in tuple('st')
                ):
                    word = word[:-3]

        # Step 5
        if word[-1] == 'e':
            if len(word[r2_start:]) >= 1 or (
                len(word[r1_start:]) >= 1
                and not self._sb_ends_in_short_syllable(word[:-1])
            ):
                word = word[:-1]
        elif word[-1] == 'l':
            if len(word[r2_start:]) >= 1 and word[-2] == 'l':
                word = word[:-1]

        # Change 'Y' back to 'y' if it survived stemming
        for i in range(0, len(word)):
            if word[i] == 'Y':
                word = word[:i] + 'y' + word[i + 1 :]

        return word