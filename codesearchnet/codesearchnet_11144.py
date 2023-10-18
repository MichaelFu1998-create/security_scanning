def docs_of_words(self):
        r"""Return the docs in the corpus, with sentences flattened.

        Each list within the corpus represents all the words of that document.
        Thus the sentence level of lists has been flattened.

        Returns
        -------
        [[str]]
            The docs in the corpus as a list of list of strs

        Example
        -------
        >>> tqbf = 'The quick brown fox jumped over the lazy dog.\n'
        >>> tqbf += 'And then it slept.\n And the dog ran off.'
        >>> corp = Corpus(tqbf)
        >>> corp.docs_of_words()
        [['The', 'quick', 'brown', 'fox', 'jumped', 'over', 'the', 'lazy',
        'dog.', 'And', 'then', 'it', 'slept.', 'And', 'the', 'dog', 'ran',
        'off.']]
        >>> len(corp.docs_of_words())
        1

        """
        return [
            [words for sents in doc for words in sents] for doc in self.corpus
        ]