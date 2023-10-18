def encode(self, word):
        """Return the Russell Index (integer output) of a word.

        Parameters
        ----------
        word : str
            The word to transform

        Returns
        -------
        int
            The Russell Index value

        Examples
        --------
        >>> pe = RussellIndex()
        >>> pe.encode('Christopher')
        3813428
        >>> pe.encode('Niall')
        715
        >>> pe.encode('Smith')
        3614
        >>> pe.encode('Schmidt')
        3614

        """
        word = unicode_normalize('NFKD', text_type(word.upper()))
        word = word.replace('ß', 'SS')
        word = word.replace('GH', '')  # discard gh (rule 3)
        word = word.rstrip('SZ')  # discard /[sz]$/ (rule 3)

        # translate according to Russell's mapping
        word = ''.join(c for c in word if c in self._uc_set)
        sdx = word.translate(self._trans)

        # remove any 1s after the first occurrence
        one = sdx.find('1') + 1
        if one:
            sdx = sdx[:one] + ''.join(c for c in sdx[one:] if c != '1')

        # remove repeating characters
        sdx = self._delete_consecutive_repeats(sdx)

        # return as an int
        return int(sdx) if sdx else float('NaN')