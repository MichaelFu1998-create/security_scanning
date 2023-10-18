def _apply_final_rules(self, phonetic, final_rules, language_arg, strip):
        """Apply a set of final rules to the phonetic encoding.

        Parameters
        ----------
        phonetic : str
            The term to which to apply the final rules
        final_rules : tuple
            The set of final phonetic transform regexps
        language_arg : int
            An integer representing the target language of the phonetic
            encoding
        strip : bool
            Flag to indicate whether to normalize the language attributes

        Returns
        -------
        str
            A Beider-Morse phonetic code

        """
        # optimization to save time
        if not final_rules:
            return phonetic

        # expand the result
        phonetic = self._expand_alternates(phonetic)
        phonetic_array = phonetic.split('|')

        for k in range(len(phonetic_array)):
            phonetic = phonetic_array[k]
            phonetic2 = ''
            phoneticx = self._normalize_lang_attrs(phonetic, True)

            i = 0
            while i < len(phonetic):
                found = False

                if phonetic[i] == '[':  # skip over language attribute
                    attrib_start = i
                    i += 1
                    while True:
                        if phonetic[i] == ']':
                            i += 1
                            phonetic2 += phonetic[attrib_start:i]
                            break
                        i += 1
                    continue

                for rule in final_rules:
                    pattern = rule[_PATTERN_POS]
                    pattern_length = len(pattern)
                    lcontext = rule[_LCONTEXT_POS]
                    rcontext = rule[_RCONTEXT_POS]

                    right = '^' + rcontext
                    left = lcontext + '$'

                    # check to see if next sequence in phonetic matches the
                    # string in the rule
                    if (pattern_length > len(phoneticx) - i) or phoneticx[
                        i : i + pattern_length
                    ] != pattern:
                        continue

                    # check that right context is satisfied
                    if rcontext != '':
                        if not search(right, phoneticx[i + pattern_length :]):
                            continue

                    # check that left context is satisfied
                    if lcontext != '':
                        if not search(left, phoneticx[:i]):
                            continue

                    # check for incompatible attributes
                    candidate = self._apply_rule_if_compat(
                        phonetic2, rule[_PHONETIC_POS], language_arg
                    )
                    # The below condition shouldn't ever be false
                    if candidate is not None:  # pragma: no branch
                        phonetic2 = candidate
                        found = True
                        break

                if not found:
                    # character in name for which there is no substitution in
                    # the table
                    phonetic2 += phonetic[i]
                    pattern_length = 1

                i += pattern_length

            phonetic_array[k] = self._expand_alternates(phonetic2)

        phonetic = '|'.join(phonetic_array)
        if strip:
            phonetic = self._normalize_lang_attrs(phonetic, True)

        if '|' in phonetic:
            phonetic = '(' + self._remove_dupes(phonetic) + ')'

        return phonetic