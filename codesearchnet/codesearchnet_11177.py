def encode(self, word, max_length=6, zero_pad=True):
        """Return the Daitch-Mokotoff Soundex code for a word.

        Parameters
        ----------
        word : str
            The word to transform
        max_length : int
            The length of the code returned (defaults to 6; must be between 6
            and 64)
        zero_pad : bool
            Pad the end of the return value with 0s to achieve a max_length
            string

        Returns
        -------
        str
            The Daitch-Mokotoff Soundex value

        Examples
        --------
        >>> pe = DaitchMokotoff()
        >>> sorted(pe.encode('Christopher'))
        ['494379', '594379']
        >>> pe.encode('Niall')
        {'680000'}
        >>> pe.encode('Smith')
        {'463000'}
        >>> pe.encode('Schmidt')
        {'463000'}

        >>> sorted(pe.encode('The quick brown fox', max_length=20,
        ... zero_pad=False))
        ['35457976754', '3557976754']

        """
        dms = ['']  # initialize empty code list

        # Require a max_length of at least 6 and not more than 64
        if max_length != -1:
            max_length = min(max(6, max_length), 64)
        else:
            max_length = 64

        # uppercase, normalize, decompose, and filter non-A-Z
        word = unicode_normalize('NFKD', text_type(word.upper()))
        word = word.replace('ß', 'SS')
        word = ''.join(c for c in word if c in self._uc_set)

        # Nothing to convert, return base case
        if not word:
            if zero_pad:
                return {'0' * max_length}
            return {'0'}

        pos = 0
        while pos < len(word):
            # Iterate through _dms_order, which specifies the possible
            # substrings for which codes exist in the Daitch-Mokotoff coding
            for sstr in self._dms_order[word[pos]]:  # pragma: no branch
                if word[pos:].startswith(sstr):
                    # Having determined a valid substring start, retrieve the
                    # code
                    dm_val = self._dms_table[sstr]

                    # Having retried the code (triple), determine the correct
                    # positional variant (first, pre-vocalic, elsewhere)
                    if pos == 0:
                        dm_val = dm_val[0]
                    elif (
                        pos + len(sstr) < len(word)
                        and word[pos + len(sstr)] in self._uc_v_set
                    ):
                        dm_val = dm_val[1]
                    else:
                        dm_val = dm_val[2]

                    # Build the code strings
                    if isinstance(dm_val, tuple):
                        dms = [_ + text_type(dm_val[0]) for _ in dms] + [
                            _ + text_type(dm_val[1]) for _ in dms
                        ]
                    else:
                        dms = [_ + text_type(dm_val) for _ in dms]
                    pos += len(sstr)
                    break

        # Filter out double letters and _ placeholders
        dms = (
            ''.join(c for c in self._delete_consecutive_repeats(_) if c != '_')
            for _ in dms
        )

        # Trim codes and return set
        if zero_pad:
            dms = ((_ + ('0' * max_length))[:max_length] for _ in dms)
        else:
            dms = (_[:max_length] for _ in dms)
        return set(dms)