def _add_to_ngcorpus(self, corpus, words, count):
        """Build up a corpus entry recursively.

        Parameters
        ----------
        corpus : Corpus
            The corpus
        words : [str]
            Words to add to the corpus
        count : int
            Count of words

        """
        if words[0] not in corpus:
            corpus[words[0]] = Counter()

        if len(words) == 1:
            corpus[words[0]][None] += count
        else:
            self._add_to_ngcorpus(corpus[words[0]], words[1:], count)