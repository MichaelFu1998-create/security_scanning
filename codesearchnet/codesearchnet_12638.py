def create_document_dictionary(self, document, document_key=None,
                                                        owner_document=None):
        """
        Given document generates a dictionary representation of the document.
        Includes the widget for each for each field in the document.
        """
        doc_dict = self.create_doc_dict(document, document_key, owner_document)

        for doc_key, doc_field in doc_dict.items():
            # Base fields should not be evaluated
            if doc_key.startswith("_"):
                continue

            if isinstance(doc_field, ListField):
                doc_dict[doc_key] = self.create_list_dict(document, doc_field, doc_key)

            elif isinstance(doc_field, EmbeddedDocumentField):
                doc_dict[doc_key] = self.create_document_dictionary(doc_dict[doc_key].document_type_obj,
                                                                    doc_key)
            else:
                doc_dict[doc_key] = {"_document": document,
                                     "_key": doc_key,
                                     "_document_field": doc_field,
                                     "_widget": get_widget(doc_dict[doc_key], getattr(doc_field, 'disabled', False))}

        return doc_dict