def idf(self, term, transform=None):
        r"""Calculate the Inverse Document Frequency of a term in the corpus.

        Parameters
        ----------
        term : str
            The term to calculate the IDF of
        transform : function
            A function to apply to each document term before checking for the
            presence of term

        Returns
        -------
        float
            The IDF

        Examples
        --------
        >>> tqbf = 'The quick brown fox jumped over the lazy dog.\n\n'
        >>> tqbf += 'And then it slept.\n\n And the dog ran off.'
        >>> corp = Corpus(tqbf)
        >>> print(corp.docs())
        [[['The', 'quick', 'brown', 'fox', 'jumped', 'over', 'the', 'lazy',
        'dog.']],
        [['And', 'then', 'it', 'slept.']],
        [['And', 'the', 'dog', 'ran', 'off.']]]
        >>> round(corp.idf('dog'), 10)
        0.4771212547
        >>> round(corp.idf('the'), 10)
        0.1760912591

        """
        docs_with_term = 0
        docs = self.docs_of_words()
        for doc in docs:
            doc_set = set(doc)
            if transform:
                transformed_doc = []
                for word in doc_set:
                    transformed_doc.append(transform(word))
                doc_set = set(transformed_doc)

            if term in doc_set:
                docs_with_term += 1

        if docs_with_term == 0:
            return float('inf')

        return log10(len(docs) / docs_with_term)