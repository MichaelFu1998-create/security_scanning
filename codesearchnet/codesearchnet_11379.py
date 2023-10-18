def stem(self, word, early_english=False):
        """Return Porter stem.

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
        >>> stmr = Porter()
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

        # Return word if stem is shorter than 2
        if len(word) < 3:
            return word

        # Re-map consonantal y to Y (Y will be C, y will be V)
        if word[0] == 'y':
            word = 'Y' + word[1:]
        for i in range(1, len(word)):
            if word[i] == 'y' and word[i - 1] in self._vowels:
                word = word[:i] + 'Y' + word[i + 1 :]

        # Step 1a
        if word[-1] == 's':
            if word[-4:] == 'sses':
                word = word[:-2]
            elif word[-3:] == 'ies':
                word = word[:-2]
            elif word[-2:] == 'ss':
                pass
            else:
                word = word[:-1]

        # Step 1b
        step1b_flag = False
        if word[-3:] == 'eed':
            if self._m_degree(word[:-3]) > 0:
                word = word[:-1]
        elif word[-2:] == 'ed':
            if self._has_vowel(word[:-2]):
                word = word[:-2]
                step1b_flag = True
        elif word[-3:] == 'ing':
            if self._has_vowel(word[:-3]):
                word = word[:-3]
                step1b_flag = True
        elif early_english:
            if word[-3:] == 'est':
                if self._has_vowel(word[:-3]):
                    word = word[:-3]
                    step1b_flag = True
            elif word[-3:] == 'eth':
                if self._has_vowel(word[:-3]):
                    word = word[:-3]
                    step1b_flag = True

        if step1b_flag:
            if word[-2:] in {'at', 'bl', 'iz'}:
                word += 'e'
            elif self._ends_in_doubled_cons(word) and word[-1] not in {
                'l',
                's',
                'z',
            }:
                word = word[:-1]
            elif self._m_degree(word) == 1 and self._ends_in_cvc(word):
                word += 'e'

        # Step 1c
        if word[-1] in {'Y', 'y'} and self._has_vowel(word[:-1]):
            word = word[:-1] + 'i'

        # Step 2
        if len(word) > 1:
            if word[-2] == 'a':
                if word[-7:] == 'ational':
                    if self._m_degree(word[:-7]) > 0:
                        word = word[:-5] + 'e'
                elif word[-6:] == 'tional':
                    if self._m_degree(word[:-6]) > 0:
                        word = word[:-2]
            elif word[-2] == 'c':
                if word[-4:] in {'enci', 'anci'}:
                    if self._m_degree(word[:-4]) > 0:
                        word = word[:-1] + 'e'
            elif word[-2] == 'e':
                if word[-4:] == 'izer':
                    if self._m_degree(word[:-4]) > 0:
                        word = word[:-1]
            elif word[-2] == 'g':
                if word[-4:] == 'logi':
                    if self._m_degree(word[:-4]) > 0:
                        word = word[:-1]
            elif word[-2] == 'l':
                if word[-3:] == 'bli':
                    if self._m_degree(word[:-3]) > 0:
                        word = word[:-1] + 'e'
                elif word[-4:] == 'alli':
                    if self._m_degree(word[:-4]) > 0:
                        word = word[:-2]
                elif word[-5:] == 'entli':
                    if self._m_degree(word[:-5]) > 0:
                        word = word[:-2]
                elif word[-3:] == 'eli':
                    if self._m_degree(word[:-3]) > 0:
                        word = word[:-2]
                elif word[-5:] == 'ousli':
                    if self._m_degree(word[:-5]) > 0:
                        word = word[:-2]
            elif word[-2] == 'o':
                if word[-7:] == 'ization':
                    if self._m_degree(word[:-7]) > 0:
                        word = word[:-5] + 'e'
                elif word[-5:] == 'ation':
                    if self._m_degree(word[:-5]) > 0:
                        word = word[:-3] + 'e'
                elif word[-4:] == 'ator':
                    if self._m_degree(word[:-4]) > 0:
                        word = word[:-2] + 'e'
            elif word[-2] == 's':
                if word[-5:] == 'alism':
                    if self._m_degree(word[:-5]) > 0:
                        word = word[:-3]
                elif word[-7:] in {'iveness', 'fulness', 'ousness'}:
                    if self._m_degree(word[:-7]) > 0:
                        word = word[:-4]
            elif word[-2] == 't':
                if word[-5:] == 'aliti':
                    if self._m_degree(word[:-5]) > 0:
                        word = word[:-3]
                elif word[-5:] == 'iviti':
                    if self._m_degree(word[:-5]) > 0:
                        word = word[:-3] + 'e'
                elif word[-6:] == 'biliti':
                    if self._m_degree(word[:-6]) > 0:
                        word = word[:-5] + 'le'

        # Step 3
        if word[-5:] in 'icate':
            if self._m_degree(word[:-5]) > 0:
                word = word[:-3]
        elif word[-5:] == 'ative':
            if self._m_degree(word[:-5]) > 0:
                word = word[:-5]
        elif word[-5:] in {'alize', 'iciti'}:
            if self._m_degree(word[:-5]) > 0:
                word = word[:-3]
        elif word[-4:] == 'ical':
            if self._m_degree(word[:-4]) > 0:
                word = word[:-2]
        elif word[-3:] == 'ful':
            if self._m_degree(word[:-3]) > 0:
                word = word[:-3]
        elif word[-4:] == 'ness':
            if self._m_degree(word[:-4]) > 0:
                word = word[:-4]

        # Step 4
        if word[-2:] == 'al':
            if self._m_degree(word[:-2]) > 1:
                word = word[:-2]
        elif word[-4:] in {'ance', 'ence'}:
            if self._m_degree(word[:-4]) > 1:
                word = word[:-4]
        elif word[-2:] in {'er', 'ic'}:
            if self._m_degree(word[:-2]) > 1:
                word = word[:-2]
        elif word[-4:] in {'able', 'ible'}:
            if self._m_degree(word[:-4]) > 1:
                word = word[:-4]
        elif word[-3:] == 'ant':
            if self._m_degree(word[:-3]) > 1:
                word = word[:-3]
        elif word[-5:] == 'ement':
            if self._m_degree(word[:-5]) > 1:
                word = word[:-5]
        elif word[-4:] == 'ment':
            if self._m_degree(word[:-4]) > 1:
                word = word[:-4]
        elif word[-3:] == 'ent':
            if self._m_degree(word[:-3]) > 1:
                word = word[:-3]
        elif word[-4:] in {'sion', 'tion'}:
            if self._m_degree(word[:-3]) > 1:
                word = word[:-3]
        elif word[-2:] == 'ou':
            if self._m_degree(word[:-2]) > 1:
                word = word[:-2]
        elif word[-3:] in {'ism', 'ate', 'iti', 'ous', 'ive', 'ize'}:
            if self._m_degree(word[:-3]) > 1:
                word = word[:-3]

        # Step 5a
        if word[-1] == 'e':
            if self._m_degree(word[:-1]) > 1:
                word = word[:-1]
            elif self._m_degree(word[:-1]) == 1 and not self._ends_in_cvc(
                word[:-1]
            ):
                word = word[:-1]

        # Step 5b
        if word[-2:] == 'll' and self._m_degree(word) > 1:
            word = word[:-1]

        # Change 'Y' back to 'y' if it survived stemming
        for i in range(len(word)):
            if word[i] == 'Y':
                word = word[:i] + 'y' + word[i + 1 :]

        return word