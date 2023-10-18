def encode(self, word):
        """Return the Naval Research Laboratory phonetic encoding of a word.

        Parameters
        ----------
        word : str
            The word to transform

        Returns
        -------
        str
            The NRL phonetic encoding

        Examples
        --------
        >>> pe = NRL()
        >>> pe.encode('the')
        'DHAX'
        >>> pe.encode('round')
        'rAWnd'
        >>> pe.encode('quick')
        'kwIHk'
        >>> pe.encode('eaten')
        'IYtEHn'
        >>> pe.encode('Smith')
        'smIHTH'
        >>> pe.encode('Larsen')
        'lAArsEHn'

        """

        def _to_regex(pattern, left_match=True):
            new_pattern = ''
            replacements = {
                '#': '[AEIOU]+',
                ':': '[BCDFGHJKLMNPQRSTVWXYZ]*',
                '^': '[BCDFGHJKLMNPQRSTVWXYZ]',
                '.': '[BDVGJLMNTWZ]',
                '%': '(ER|E|ES|ED|ING|ELY)',
                '+': '[EIY]',
                ' ': '^',
            }
            for char in pattern:
                new_pattern += (
                    replacements[char] if char in replacements else char
                )

            if left_match:
                new_pattern += '$'
                if '^' not in pattern:
                    new_pattern = '^.*' + new_pattern
            else:
                new_pattern = '^' + new_pattern.replace('^', '$')
                if '$' not in new_pattern:
                    new_pattern += '.*$'

            return new_pattern

        word = word.upper()

        pron = ''
        pos = 0
        while pos < len(word):
            left_orig = word[:pos]
            right_orig = word[pos:]
            first = word[pos] if word[pos] in self._rules else ' '
            for rule in self._rules[first]:
                left, match, right, out = rule
                if right_orig.startswith(match):
                    if left:
                        l_pattern = _to_regex(left, left_match=True)
                    if right:
                        r_pattern = _to_regex(right, left_match=False)
                    if (not left or re_match(l_pattern, left_orig)) and (
                        not right
                        or re_match(r_pattern, right_orig[len(match) :])
                    ):
                        pron += out
                        pos += len(match)
                        break
            else:
                pron += word[pos]
                pos += 1

        return pron