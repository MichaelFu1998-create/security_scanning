def tf(self, term):
        r"""Return term frequency.

        Parameters
        ----------
        term : str
            The term for which to calculate tf

        Returns
        -------
        float
            The term frequency (tf)

        Raises
        ------
        ValueError
            tf can only calculate the frequency of individual words

        Examples
        --------
        >>> tqbf = 'The quick brown fox jumped over the lazy dog.\n'
        >>> tqbf += 'And then it slept.\n And the dog ran off.'
        >>> ngcorp = NGramCorpus(Corpus(tqbf))
        >>> NGramCorpus(Corpus(tqbf)).tf('the')
        1.3010299956639813
        >>> NGramCorpus(Corpus(tqbf)).tf('fox')
        1.0

        """
        if ' ' in term:
            raise ValueError(
                'tf can only calculate the term frequency of individual words'
            )
        tcount = self.get_count(term)
        if tcount == 0:
            return 0.0
        return 1 + log10(tcount)