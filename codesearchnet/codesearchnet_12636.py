def create_doc_dict(self, document, doc_key=None, owner_document=None):
        """
        Generate a dictionary representation of the document.  (no recursion)

        DO NOT CALL DIRECTLY
        """
        # Get doc field for top level documents
        if owner_document:
            doc_field = owner_document._fields.get(doc_key, None) if doc_key else None
        else:
            doc_field = document._fields.get(doc_key, None) if doc_key else None

        # Generate the base fields for the document
        doc_dict = {"_document": document if owner_document is None else owner_document,
                    "_key": document.__class__.__name__.lower() if doc_key is None else doc_key,
                    "_document_field": doc_field}

        if not isinstance(document, TopLevelDocumentMetaclass) and doc_key:
            doc_dict.update({"_field_type": EmbeddedDocumentField})

        for key, field in document._fields.items():
            doc_dict[key] = field

        return doc_dict