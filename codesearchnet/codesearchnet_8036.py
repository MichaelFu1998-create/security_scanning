def add_document(self, doc_id, nosave=False, score=1.0, payload=None,
                     replace=False, partial=False, language=None, **fields):
        """
        Add a single document to the index.

        ### Parameters

        - **doc_id**: the id of the saved document.
        - **nosave**: if set to true, we just index the document, and don't save a copy of it. This means that searches will just return ids.
        - **score**: the document ranking, between 0.0 and 1.0 
        - **payload**: optional inner-index payload we can save for fast access in scoring functions
        - **replace**: if True, and the document already is in the index, we perform an update and reindex the document
        - **partial**: if True, the fields specified will be added to the existing document.
                       This has the added benefit that any fields specified with `no_index`
                       will not be reindexed again. Implies `replace`
        - **language**: Specify the language used for document tokenization.
        - **fields** kwargs dictionary of the document fields to be saved and/or indexed. 
                     NOTE: Geo points shoule be encoded as strings of "lon,lat"
        """
        return self._add_document(doc_id, conn=None, nosave=nosave, score=score, 
                                  payload=payload, replace=replace,
                                  partial=partial, language=language, **fields)