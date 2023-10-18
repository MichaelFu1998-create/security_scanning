def stem(
        self,
        word,
        max_word_length=20,
        max_acro_length=8,
        return_rule_no=False,
        var='standard',
    ):
        """Return UEA-Lite stem.

        Parameters
        ----------
        word : str
            The word to stem
        max_word_length : int
            The maximum word length allowed
        max_acro_length : int
            The maximum acronym length allowed
        return_rule_no : bool
            If True, returns the stem along with rule number
        var : str
            Variant rules to use:

                - ``Adams`` to use Jason Adams' rules
                - ``Perl`` to use the original Perl rules

        Returns
        -------
        str or (str, int)
            Word stem

        Examples
        --------
        >>> uealite('readings')
        'read'
        >>> uealite('insulted')
        'insult'
        >>> uealite('cussed')
        'cuss'
        >>> uealite('fancies')
        'fancy'
        >>> uealite('eroded')
        'erode'

        """

        def _stem_with_duplicate_character_check(word, del_len):
            if word[-1] == 's':
                del_len += 1
            stemmed_word = word[:-del_len]
            if re_match(r'.*(\w)\1$', stemmed_word):
                stemmed_word = stemmed_word[:-1]
            return stemmed_word

        def _stem(word):
            stemmed_word = word
            rule_no = 0

            if not word:
                return word, 0
            if word in self._problem_words or (
                word == 'menses' and var == 'Adams'
            ):
                return word, 90
            if max_word_length and len(word) > max_word_length:
                return word, 95

            if "'" in word:
                if word[-2:] in {"'s", "'S"}:
                    stemmed_word = word[:-2]
                if word[-1:] == "'":
                    stemmed_word = word[:-1]
                stemmed_word = stemmed_word.replace("n't", 'not')
                stemmed_word = stemmed_word.replace("'ve", 'have')
                stemmed_word = stemmed_word.replace("'re", 'are')
                stemmed_word = stemmed_word.replace("'m", 'am')
                return stemmed_word, 94

            if word.isdigit():
                return word, 90.3
            else:
                hyphen = word.find('-')
                if len(word) > hyphen > 0:
                    if (
                        word[:hyphen].isalpha()
                        and word[hyphen + 1 :].isalpha()
                    ):
                        return word, 90.2
                    else:
                        return word, 90.1
                elif '_' in word:
                    return word, 90
                elif word[-1] == 's' and word[:-1].isupper():
                    if var == 'Adams' and len(word) - 1 > max_acro_length:
                        return word, 96
                    return word[:-1], 91.1
                elif word.isupper():
                    if var == 'Adams' and len(word) > max_acro_length:
                        return word, 96
                    return word, 91
                elif re_match(r'^.*[A-Z].*[A-Z].*$', word):
                    return word, 92
                elif word[0].isupper():
                    return word, 93
                elif var == 'Adams' and re_match(
                    r'^[a-z](|[rl])(ing|ed)$', word
                ):
                    return word, 97

            for n in range(7, 1, -1):
                if word[-n:] in self._rules[var][n]:
                    rule_no, del_len, add_str = self._rules[var][n][word[-n:]]
                    if del_len:
                        stemmed_word = word[:-del_len]
                    else:
                        stemmed_word = word
                    if add_str:
                        stemmed_word += add_str
                    break

            if not rule_no:
                if re_match(r'.*\w\wings?$', word):  # rule 58
                    stemmed_word = _stem_with_duplicate_character_check(
                        word, 3
                    )
                    rule_no = 58
                elif re_match(r'.*\w\weds?$', word):  # rule 62
                    stemmed_word = _stem_with_duplicate_character_check(
                        word, 2
                    )
                    rule_no = 62
                elif word[-1] == 's':  # rule 68
                    stemmed_word = word[:-1]
                    rule_no = 68

            return stemmed_word, rule_no

        stem, rule_no = _stem(word)
        if return_rule_no:
            return stem, rule_no
        return stem