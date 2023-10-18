def corpus_importer(self, corpus, n_val=1, bos='_START_', eos='_END_'):
        r"""Fill in self.ngcorpus from a Corpus argument.

        Parameters
        ----------
        corpus :Corpus
            The Corpus from which to initialize the n-gram corpus
        n_val : int
            Maximum n value for n-grams
        bos : str
            String to insert as an indicator of beginning of sentence
        eos : str
            String to insert as an indicator of end of sentence

        Raises
        ------
        TypeError
            Corpus argument of the Corpus class required.

        Example
        -------
        >>> tqbf = 'The quick brown fox jumped over the lazy dog.\n'
        >>> tqbf += 'And then it slept.\n And the dog ran off.'
        >>> ngcorp = NGramCorpus()
        >>> ngcorp.corpus_importer(Corpus(tqbf))

        """
        if not corpus or not isinstance(corpus, Corpus):
            raise TypeError('Corpus argument of the Corpus class required.')

        sentences = corpus.sents()

        for sent in sentences:
            ngs = Counter(sent)
            for key in ngs.keys():
                self._add_to_ngcorpus(self.ngcorpus, [key], ngs[key])

            if n_val > 1:
                if bos and bos != '':
                    sent = [bos] + sent
                if eos and eos != '':
                    sent += [eos]
                for i in range(2, n_val + 1):
                    for j in range(len(sent) - i + 1):
                        self._add_to_ngcorpus(
                            self.ngcorpus, sent[j : j + i], 1
                        )