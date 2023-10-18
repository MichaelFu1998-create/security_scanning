def _phonetic(
        self,
        term,
        name_mode,
        rules,
        final_rules1,
        final_rules2,
        language_arg=0,
        concat=False,
    ):
        """Return the Beider-Morse encoding(s) of a term.

        Parameters
        ----------
        term : str
            The term to encode via Beider-Morse
        name_mode : str
            The name mode of the algorithm: ``gen`` (default),
            ``ash`` (Ashkenazi), or ``sep`` (Sephardic)
        rules : tuple
            The set of initial phonetic transform regexps
        final_rules1 : tuple
            The common set of final phonetic transform regexps
        final_rules2 : tuple
            The specific set of final phonetic transform regexps
        language_arg : int
            The language of the term
        concat : bool
            A flag to indicate concatenation

        Returns
        -------
        str
            A Beider-Morse phonetic code

        """
        term = term.replace('-', ' ').strip()

        if name_mode == 'gen':  # generic case
            # discard and concatenate certain words if at the start of the name
            for pfx in BMDATA['gen']['discards']:
                if term.startswith(pfx):
                    remainder = term[len(pfx) :]
                    combined = pfx[:-1] + remainder
                    result = (
                        self._redo_language(
                            remainder,
                            name_mode,
                            rules,
                            final_rules1,
                            final_rules2,
                            concat,
                        )
                        + '-'
                        + self._redo_language(
                            combined,
                            name_mode,
                            rules,
                            final_rules1,
                            final_rules2,
                            concat,
                        )
                    )
                    return result

        words = (
            term.split()
        )  # create array of the individual words in the name
        words2 = []

        if name_mode == 'sep':  # Sephardic case
            # for each word in the name, delete portions of word preceding
            # apostrophe
            # ex: d'avila d'aguilar --> avila aguilar
            # also discard certain words in the name

            # note that we can never get a match on "de la" because we are
            # checking single words below
            # this is a bug, but I won't try to fix it now

            for word in words:
                word = word[word.rfind('\'') + 1 :]
                if word not in BMDATA['sep']['discards']:
                    words2.append(word)

        elif name_mode == 'ash':  # Ashkenazic case
            # discard certain words if at the start of the name
            if len(words) > 1 and words[0] in BMDATA['ash']['discards']:
                words2 = words[1:]
            else:
                words2 = list(words)
        else:
            words2 = list(words)

        if concat:
            # concatenate the separate words of a multi-word name
            # (normally used for exact matches)
            term = ' '.join(words2)
        elif len(words2) == 1:  # not a multi-word name
            term = words2[0]
        else:
            # encode each word in a multi-word name separately
            # (normally used for approx matches)
            result = '-'.join(
                [
                    self._redo_language(
                        w, name_mode, rules, final_rules1, final_rules2, concat
                    )
                    for w in words2
                ]
            )
            return result

        term_length = len(term)

        # apply language rules to map to phonetic alphabet
        phonetic = ''
        skip = 0
        for i in range(term_length):
            if skip:
                skip -= 1
                continue
            found = False
            for rule in rules:
                pattern = rule[_PATTERN_POS]
                pattern_length = len(pattern)
                lcontext = rule[_LCONTEXT_POS]
                rcontext = rule[_RCONTEXT_POS]

                # check to see if next sequence in input matches the string in
                # the rule
                if (pattern_length > term_length - i) or (
                    term[i : i + pattern_length] != pattern
                ):  # no match
                    continue

                right = '^' + rcontext
                left = lcontext + '$'

                # check that right context is satisfied
                if rcontext != '':
                    if not search(right, term[i + pattern_length :]):
                        continue

                # check that left context is satisfied
                if lcontext != '':
                    if not search(left, term[:i]):
                        continue

                # check for incompatible attributes
                candidate = self._apply_rule_if_compat(
                    phonetic, rule[_PHONETIC_POS], language_arg
                )
                # The below condition shouldn't ever be false
                if candidate is not None:  # pragma: no branch
                    phonetic = candidate
                    found = True
                    break

            if (
                not found
            ):  # character in name that is not in table -- e.g., space
                pattern_length = 1
            skip = pattern_length - 1

        # apply final rules on phonetic-alphabet,
        # doing a substitution of certain characters
        phonetic = self._apply_final_rules(
            phonetic, final_rules1, language_arg, False
        )  # apply common rules
        # final_rules1 are the common approx rules,
        # final_rules2 are approx rules for specific language
        phonetic = self._apply_final_rules(
            phonetic, final_rules2, language_arg, True
        )  # apply lang specific rules

        return phonetic