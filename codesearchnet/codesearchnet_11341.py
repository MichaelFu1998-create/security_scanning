def encode(self, word):
        """Return the Parmar-Kumbharana encoding of a word.

        Parameters
        ----------
        word : str
            The word to transform

        Returns
        -------
        str
            The Parmar-Kumbharana encoding

        Examples
        --------
        >>> pe = ParmarKumbharana()
        >>> pe.encode('Gough')
        'GF'
        >>> pe.encode('pneuma')
        'NM'
        >>> pe.encode('knight')
        'NT'
        >>> pe.encode('trice')
        'TRS'
        >>> pe.encode('judge')
        'JJ'

        """
        word = word.upper()  # Rule 3
        word = self._delete_consecutive_repeats(word)  # Rule 4

        # Rule 5
        i = 0
        while i < len(word):
            for match_len in range(4, 1, -1):
                if word[i : i + match_len] in self._rules[match_len]:
                    repl = self._rules[match_len][word[i : i + match_len]]
                    word = word[:i] + repl + word[i + match_len :]
                    i += len(repl)
                    break
            else:
                i += 1

        word = word[:1] + word[1:].translate(self._del_trans)  # Rule 6
        return word