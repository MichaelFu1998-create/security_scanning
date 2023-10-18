def encode(self, word, max_length=4, zero_pad=True):
        """Return the Oxford Name Compression Algorithm (ONCA) code for a word.

        Parameters
        ----------
        word : str
            The word to transform
        max_length : int
            The maximum length (default 5) of the code to return
        zero_pad : bool
            Pad the end of the return value with 0s to achieve a max_length
            string

        Returns
        -------
        str
            The ONCA code

        Examples
        --------
        >>> pe = ONCA()
        >>> pe.encode('Christopher')
        'C623'
        >>> pe.encode('Niall')
        'N400'
        >>> pe.encode('Smith')
        'S530'
        >>> pe.encode('Schmidt')
        'S530'

        """
        # In the most extreme case, 3 characters of NYSIIS input can be
        # compressed to one character of output, so give it triple the
        # max_length.
        return self._soundex.encode(
            self._nysiis.encode(word, max_length=max_length * 3),
            max_length,
            zero_pad=zero_pad,
        )