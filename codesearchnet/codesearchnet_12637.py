def create_list_dict(self, document, list_field, doc_key):
        """
        Genereates a dictionary representation of the list field. Document
        should be the document the list_field comes from.

        DO NOT CALL DIRECTLY
        """
        list_dict = {"_document": document}

        if isinstance(list_field.field, EmbeddedDocumentField):
            list_dict.update(self.create_document_dictionary(document=list_field.field.document_type_obj,
                                                             owner_document=document))

        # Set the list_dict after it may have been updated
        list_dict.update({"_document_field": list_field.field,
                          "_key": doc_key,
                          "_field_type": ListField,
                          "_widget": get_widget(list_field.field),
                          "_value": getattr(document, doc_key, None)})

        return list_dict