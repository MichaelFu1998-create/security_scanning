def process_document(self, document, form_key, passed_key):
        """
        Given the form_key will evaluate the document and set values correctly for
        the document given.
        """
        if passed_key is not None:
            current_key, remaining_key_array = trim_field_key(document, passed_key)
        else:
            current_key, remaining_key_array = trim_field_key(document, form_key)

        key_array_digit = remaining_key_array[-1] if remaining_key_array and has_digit(remaining_key_array) else None
        remaining_key = make_key(remaining_key_array)

        if current_key.lower() == 'id':
            raise KeyError(u"Mongonaut does not work with models which have fields beginning with id_")

        # Create boolean checks to make processing document easier
        is_embedded_doc = (isinstance(document._fields.get(current_key, None), EmbeddedDocumentField)
                          if hasattr(document, '_fields') else False)
        is_list = not key_array_digit is None
        key_in_fields = current_key in document._fields.keys() if hasattr(document, '_fields') else False

        # This ensures you only go through each documents keys once, and do not duplicate data
        if key_in_fields:
            if is_embedded_doc:
                self.set_embedded_doc(document, form_key, current_key, remaining_key)
            elif is_list:
                self.set_list_field(document, form_key, current_key, remaining_key, key_array_digit)
            else:
                value = translate_value(document._fields[current_key],
                                        self.form.cleaned_data[form_key])
                setattr(document, current_key, value)