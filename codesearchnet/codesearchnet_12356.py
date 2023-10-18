def fit_transform(self, raw_documents, y=None):
        """ Learn the vocabulary dictionary and return term-document matrix.
        This is equivalent to fit followed by transform, but more efficiently
        implemented.

        Parameters
        ----------
        raw_documents : iterable
            An iterable which yields either str, unicode or file objects.

        Returns
        -------
        X : array, [n_samples, n_features]
            Document-term matrix.
        """
        documents = super(CountVectorizer, self).fit_transform(
            raw_documents=raw_documents, y=y)
        self.n = len(raw_documents)
        m = (self.transform(raw_documents) > 0).astype(int)
        m = m.sum(axis=0).A1
        self.period_ = m
        self.df_ = m / self.n
        return documents