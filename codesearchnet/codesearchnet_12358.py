def transform(self, transformer):
        """
        Add transformer to flow and apply transformer to data in flow

        Parameters
        ----------
        transformer : Transformer
            a transformer to transform data
        """
        self.transformers.append(transformer)
        from languageflow.transformer.tagged import TaggedTransformer

        if isinstance(transformer, TaggedTransformer):
            self.X, self.y = transformer.transform(self.sentences)
        if isinstance(transformer, TfidfVectorizer):
            self.X = transformer.fit_transform(self.X)
        if isinstance(transformer, CountVectorizer):
            self.X = transformer.fit_transform(self.X)
        if isinstance(transformer, NumberRemover):
            self.X = transformer.transform(self.X)

        if isinstance(transformer, MultiLabelBinarizer):
            self.y = transformer.fit_transform(self.y)