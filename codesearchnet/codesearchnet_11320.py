def encode(self, word):
        """Return the FONEM code of a word.

        Parameters
        ----------
        word : str
            The word to transform

        Returns
        -------
        str
            The FONEM code

        Examples
        --------
        >>> pe = FONEM()
        >>> pe.encode('Marchand')
        'MARCHEN'
        >>> pe.encode('Beaulieu')
        'BOLIEU'
        >>> pe.encode('Beaumont')
        'BOMON'
        >>> pe.encode('Legrand')
        'LEGREN'
        >>> pe.encode('Pelletier')
        'PELETIER'

        """
        # normalize, upper-case, and filter non-French letters
        word = unicode_normalize('NFKD', text_type(word.upper()))
        word = word.translate({198: 'AE', 338: 'OE'})
        word = ''.join(c for c in word if c in self._uc_set)

        for rule in self._rule_order:
            regex, repl = self._rule_table[rule]
            if isinstance(regex, text_type):
                word = word.replace(regex, repl)
            else:
                word = regex.sub(repl, word)

        return word