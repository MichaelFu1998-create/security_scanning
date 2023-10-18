def _apply_rule_if_compat(self, phonetic, target, language_arg):
        """Apply a phonetic regex if compatible.

        tests for compatible language rules

        to do so, apply the rule, expand the results, and detect alternatives
            with incompatible attributes

        then drop each alternative that has incompatible attributes and keep
            those that are compatible

        if there are no compatible alternatives left, return false

        otherwise return the compatible alternatives

        apply the rule

        Parameters
        ----------
        phonetic : str
            The Beider-Morse phonetic encoding (so far)
        target : str
            A proposed addition to the phonetic encoding
        language_arg : int
            An integer representing the target language of the phonetic
            encoding

        Returns
        -------
        str
            A candidate encoding

        """
        candidate = phonetic + target
        if '[' not in candidate:  # no attributes so we need test no further
            return candidate

        # expand the result, converting incompatible attributes to [0]
        candidate = self._expand_alternates(candidate)
        candidate_array = candidate.split('|')

        # drop each alternative that has incompatible attributes
        candidate = ''
        found = False

        for i in range(len(candidate_array)):
            this_candidate = candidate_array[i]
            if language_arg != 1:
                this_candidate = self._normalize_lang_attrs(
                    this_candidate + '[' + str(language_arg) + ']', False
                )
            if this_candidate != '[0]':
                found = True
                if candidate:
                    candidate += '|'
                candidate += this_candidate

        # return false if no compatible alternatives remain
        if not found:
            return None

        # return the result of applying the rule
        if '|' in candidate:
            candidate = '(' + candidate + ')'
        return candidate