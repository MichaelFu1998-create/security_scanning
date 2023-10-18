def fit_tranform(self, raw_documents):
        """
        Transform given list of raw_documents to document-term matrix in
        sparse CSR format (see scipy)
        """
        X = self.transform(raw_documents, new_document=True)
        return X