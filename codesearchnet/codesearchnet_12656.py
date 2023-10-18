def set_list_field(self, document, form_key, current_key, remaining_key, key_array_digit):
        """1. Figures out what value the list ought to have
           2. Sets the list
        """

        document_field = document._fields.get(current_key)

        # Figure out what value the list ought to have
        # None value for ListFields make mongoengine very un-happy
        list_value = translate_value(document_field.field, self.form.cleaned_data[form_key])
        if list_value is None or (not list_value and not bool(list_value)):
            return None

        current_list = getattr(document, current_key, None)

        if isinstance(document_field.field, EmbeddedDocumentField):
            embedded_list_key = u"{0}_{1}".format(current_key, key_array_digit)

            # Get the embedded document if it exists, else create it.
            embedded_list_document = self.embedded_list_docs.get(embedded_list_key, None)
            if embedded_list_document is None:
                embedded_list_document = document_field.field.document_type_obj()

            new_key, new_remaining_key_array = trim_field_key(embedded_list_document, remaining_key)
            self.process_document(embedded_list_document, form_key, new_key)

            list_value = embedded_list_document
            self.embedded_list_docs[embedded_list_key] = embedded_list_document

            if isinstance(current_list, list):
                # Do not add the same document twice
                if embedded_list_document not in current_list:
                    current_list.append(embedded_list_document)
            else:
                setattr(document, current_key, [embedded_list_document])

        elif isinstance(current_list, list):
            current_list.append(list_value)
        else:
            setattr(document, current_key, [list_value])