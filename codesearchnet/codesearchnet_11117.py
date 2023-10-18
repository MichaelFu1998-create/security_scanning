def get_count(self, ngram, corpus=None):
        r"""Get the count of an n-gram in the corpus.

        Parameters
        ----------
        ngram : str
            The n-gram to retrieve the count of from the n-gram corpus
        corpus : Corpus
            The corpus

        Returns
        -------
        int
            The n-gram count

        Examples
        --------
        >>> tqbf = 'The quick brown fox jumped over the lazy dog.\n'
        >>> tqbf += 'And then it slept.\n And the dog ran off.'
        >>> ngcorp = NGramCorpus(Corpus(tqbf))
        >>> NGramCorpus(Corpus(tqbf)).get_count('the')
        2
        >>> NGramCorpus(Corpus(tqbf)).get_count('fox')
        1

        """
        if not corpus:
            corpus = self.ngcorpus

        # if ngram is empty, we're at our leaf node and should return the
        # value in None
        if not ngram:
            return corpus[None]

        # support strings or lists/tuples by splitting strings
        if isinstance(ngram, (text_type, str)):
            ngram = text_type(ngram).split()

        # if ngram is not empty, check whether the next element is in the
        # corpus; if so, recurse--if not, return 0
        if ngram[0] in corpus:
            return self.get_count(ngram[1:], corpus[ngram[0]])
        return 0