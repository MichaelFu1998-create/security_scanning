def set_embedded_doc(self, document, form_key, current_key, remaining_key):
        """Get the existing embedded document if it exists, else created it."""

        embedded_doc = getattr(document, current_key, False)
        if not embedded_doc:
            embedded_doc = document._fields[current_key].document_type_obj()

        new_key, new_remaining_key_array = trim_field_key(embedded_doc, remaining_key)
        self.process_document(embedded_doc, form_key, make_key(new_key, new_remaining_key_array))
        setattr(document, current_key, embedded_doc)