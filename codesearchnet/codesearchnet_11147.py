def stem(self, word):
        """Return Paice-Husk stem.

        Parameters
        ----------
        word : str
            The word to stem

        Returns
        -------
        str
            Word stem

        Examples
        --------
        >>> stmr = PaiceHusk()
        >>> stmr.stem('assumption')
        'assum'
        >>> stmr.stem('verifiable')
        'ver'
        >>> stmr.stem('fancies')
        'fant'
        >>> stmr.stem('fanciful')
        'fancy'
        >>> stmr.stem('torment')
        'tor'

        """
        terminate = False
        intact = True
        while not terminate:
            for n in range(6, 0, -1):
                if word[-n:] in self._rule_table[n]:
                    accept = False
                    if len(self._rule_table[n][word[-n:]]) < 4:
                        for rule in self._rule_table[n][word[-n:]]:
                            (
                                word,
                                accept,
                                intact,
                                terminate,
                            ) = self._apply_rule(word, rule, intact, terminate)
                            if accept:
                                break
                    else:
                        rule = self._rule_table[n][word[-n:]]
                        (word, accept, intact, terminate) = self._apply_rule(
                            word, rule, intact, terminate
                        )

                    if accept:
                        break
            else:
                break

        return word