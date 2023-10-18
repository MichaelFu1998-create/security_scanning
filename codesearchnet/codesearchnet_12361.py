def fit_transform(self, raw_documents, y=None):
        """Learn vocabulary and idf, return term-document matrix.
        This is equivalent to fit followed by transform, but more efficiently
        implemented.
        Parameters
        ----------
        raw_documents : iterable
            an iterable which yields either str, unicode or file objects
        Returns
        -------
        X : sparse matrix, [n_samples, n_features]
            Tf-idf-weighted document-term matrix.
        """
        documents = super(TfidfVectorizer, self).fit_transform(
            raw_documents=raw_documents, y=y)
        count = CountVectorizer(encoding=self.encoding,
                                decode_error=self.decode_error,
                                strip_accents=self.strip_accents,
                                lowercase=self.lowercase,
                                preprocessor=self.preprocessor,
                                tokenizer=self.tokenizer,
                                stop_words=self.stop_words,
                                token_pattern=self.token_pattern,
                                ngram_range=self.ngram_range,
                                analyzer=self.analyzer,
                                max_df=self.max_df,
                                min_df=self.min_df,
                                max_features=self.max_features,
                                vocabulary=self.vocabulary_,
                                binary=self.binary,
                                dtype=self.dtype)
        count.fit_transform(raw_documents=raw_documents, y=y)
        self.period_ = count.period_
        self.df_ = count.df_
        self.n = count.n
        return documents