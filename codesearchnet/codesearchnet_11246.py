def encode(self, word, max_length=4, zero_pad=True):
        """Return the Lein code for a word.

        Parameters
        ----------
        word : str
            The word to transform
        max_length : int
            The length of the code returned (defaults to 4)
        zero_pad : bool
            Pad the end of the return value with 0s to achieve a max_length
            string

        Returns
        -------
        str
            The Lein code

        Examples
        --------
        >>> pe = Lein()
        >>> pe.encode('Christopher')
        'C351'
        >>> pe.encode('Niall')
        'N300'
        >>> pe.encode('Smith')
        'S210'
        >>> pe.encode('Schmidt')
        'S521'

        """
        # uppercase, normalize, decompose, and filter non-A-Z out
        word = unicode_normalize('NFKD', text_type(word.upper()))
        word = word.replace('ß', 'SS')
        word = ''.join(c for c in word if c in self._uc_set)

        code = word[:1]  # Rule 1
        word = word[1:].translate(self._del_trans)  # Rule 2
        word = self._delete_consecutive_repeats(word)  # Rule 3
        code += word.translate(self._trans)  # Rule 4

        if zero_pad:
            code += '0' * max_length  # Rule 4

        return code[:max_length]