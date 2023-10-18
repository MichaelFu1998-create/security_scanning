def raw(self):
        r"""Return the raw corpus.

        This is reconstructed by joining sub-components with the corpus' split
        characters

        Returns
        -------
        str
            The raw corpus

        Example
        -------
        >>> tqbf = 'The quick brown fox jumped over the lazy dog.\n'
        >>> tqbf += 'And then it slept.\n And the dog ran off.'
        >>> corp = Corpus(tqbf)
        >>> print(corp.raw())
        The quick brown fox jumped over the lazy dog.
        And then it slept.
        And the dog ran off.
        >>> len(corp.raw())
        85

        """
        doc_list = []
        for doc in self.corpus:
            sent_list = []
            for sent in doc:
                sent_list.append(' '.join(sent))
            doc_list.append(self.sent_split.join(sent_list))
            del sent_list
        return self.doc_split.join(doc_list)