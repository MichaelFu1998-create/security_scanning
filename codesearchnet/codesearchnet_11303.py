def stem(self, word):
        """Return the stem of a word according to the Schinke stemmer.

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
        >>> stmr = Schinke()
        >>> stmr.stem('atque')
        {'n': 'atque', 'v': 'atque'}
        >>> stmr.stem('census')
        {'n': 'cens', 'v': 'censu'}
        >>> stmr.stem('virum')
        {'n': 'uir', 'v': 'uiru'}
        >>> stmr.stem('populusque')
        {'n': 'popul', 'v': 'populu'}
        >>> stmr.stem('senatus')
        {'n': 'senat', 'v': 'senatu'}

        """
        word = normalize('NFKD', text_type(word.lower()))
        word = ''.join(
            c
            for c in word
            if c
            in {
                'a',
                'b',
                'c',
                'd',
                'e',
                'f',
                'g',
                'h',
                'i',
                'j',
                'k',
                'l',
                'm',
                'n',
                'o',
                'p',
                'q',
                'r',
                's',
                't',
                'u',
                'v',
                'w',
                'x',
                'y',
                'z',
            }
        )

        # Rule 2
        word = word.replace('j', 'i').replace('v', 'u')

        # Rule 3
        if word[-3:] == 'que':
            # This diverges from the paper by also returning 'que' itself
            #  unstemmed
            if word[:-3] in self._keep_que or word == 'que':
                return {'n': word, 'v': word}
            else:
                word = word[:-3]

        # Base case will mean returning the words as is
        noun = word
        verb = word

        # Rule 4
        for endlen in range(4, 0, -1):
            if word[-endlen:] in self._n_endings[endlen]:
                if len(word) - 2 >= endlen:
                    noun = word[:-endlen]
                else:
                    noun = word
                break

        for endlen in range(6, 0, -1):
            if word[-endlen:] in self._v_endings_strip[endlen]:
                if len(word) - 2 >= endlen:
                    verb = word[:-endlen]
                else:
                    verb = word
                break
            if word[-endlen:] in self._v_endings_alter[endlen]:
                if word[-endlen:] in {
                    'iuntur',
                    'erunt',
                    'untur',
                    'iunt',
                    'unt',
                }:
                    new_word = word[:-endlen] + 'i'
                    addlen = 1
                elif word[-endlen:] in {'beris', 'bor', 'bo'}:
                    new_word = word[:-endlen] + 'bi'
                    addlen = 2
                else:
                    new_word = word[:-endlen] + 'eri'
                    addlen = 3

                # Technically this diverges from the paper by considering the
                # length of the stem without the new suffix
                if len(new_word) >= 2 + addlen:
                    verb = new_word
                else:
                    verb = word
                break

        return {'n': noun, 'v': verb}