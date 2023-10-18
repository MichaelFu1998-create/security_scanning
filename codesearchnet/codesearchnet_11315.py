def stem(self, word):
        """Return Caumanns German stem.

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
        >>> stmr = Caumanns()
        >>> stmr.stem('lesen')
        'les'
        >>> stmr.stem('graues')
        'grau'
        >>> stmr.stem('buchstabieren')
        'buchstabier'

        """
        if not word:
            return ''

        upper_initial = word[0].isupper()
        word = normalize('NFC', text_type(word.lower()))

        # # Part 2: Substitution
        # 1. Change umlauts to corresponding vowels & ß to ss
        word = word.translate(self._umlauts)
        word = word.replace('ß', 'ss')

        # 2. Change second of doubled characters to *
        new_word = word[0]
        for i in range(1, len(word)):
            if new_word[i - 1] == word[i]:
                new_word += '*'
            else:
                new_word += word[i]
        word = new_word

        # 3. Replace sch, ch, ei, ie with $, §, %, &
        word = word.replace('sch', '$')
        word = word.replace('ch', '§')
        word = word.replace('ei', '%')
        word = word.replace('ie', '&')
        word = word.replace('ig', '#')
        word = word.replace('st', '!')

        # # Part 1: Recursive Context-Free Stripping
        # 1. Remove the following 7 suffixes recursively
        while len(word) > 3:
            if (len(word) > 4 and word[-2:] in {'em', 'er'}) or (
                len(word) > 5 and word[-2:] == 'nd'
            ):
                word = word[:-2]
            elif (word[-1] in {'e', 's', 'n'}) or (
                not upper_initial and word[-1] in {'t', '!'}
            ):
                word = word[:-1]
            else:
                break

        # Additional optimizations:
        if len(word) > 5 and word[-5:] == 'erin*':
            word = word[:-1]
        if word[-1] == 'z':
            word = word[:-1] + 'x'

        # Reverse substitutions:
        word = word.replace('$', 'sch')
        word = word.replace('§', 'ch')
        word = word.replace('%', 'ei')
        word = word.replace('&', 'ie')
        word = word.replace('#', 'ig')
        word = word.replace('!', 'st')

        # Expand doubled
        word = ''.join(
            [word[0]]
            + [
                word[i - 1] if word[i] == '*' else word[i]
                for i in range(1, len(word))
            ]
        )

        # Finally, convert gege to ge
        if len(word) > 4:
            word = word.replace('gege', 'ge', 1)

        return word