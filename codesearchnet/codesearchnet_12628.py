def set_form_fields(self, form_field_dict, parent_key=None, field_type=None):
        """
        Set the form fields for every key in the form_field_dict.

        Params:
          form_field_dict -- a dictionary created by get_form_field_dict
          parent_key -- the key for the previous key in the recursive call
          field_type -- used to determine what kind of field we are setting
        """
        for form_key, field_value in form_field_dict.items():
            form_key = make_key(parent_key, form_key) if parent_key is not None else form_key
            if isinstance(field_value, tuple):

                set_list_class = False
                base_key = form_key

                # Style list fields
                if ListField in (field_value.field_type, field_type):

                    # Nested lists/embedded docs need special care to get
                    # styles to work out nicely.
                    if parent_key is None or ListField == field_value.field_type:
                        if field_type != EmbeddedDocumentField:
                            field_value.widget.attrs['class'] += ' listField {0}'.format(form_key)
                        set_list_class = True
                    else:
                        field_value.widget.attrs['class'] += ' listField'

                    # Compute number value for list key
                    list_keys = [field_key for field_key in self.form.fields.keys()
                                           if has_digit(field_key)]

                    key_int = 0
                    while form_key in list_keys:
                        key_int += 1
                    form_key = make_key(form_key, key_int)

                if parent_key is not None:

                    # Get the base key for our embedded field class
                    valid_base_keys = [model_key for model_key in self.model_map_dict.keys()
                                                 if not model_key.startswith("_")]
                    while base_key not in valid_base_keys and base_key:
                        base_key = make_key(base_key, exclude_last_string=True)

                    # We need to remove the trailing number from the key
                    # so that grouping will occur on the front end when we have a list.
                    embedded_key_class = None
                    if set_list_class:
                        field_value.widget.attrs['class'] += " listField".format(base_key)
                        embedded_key_class = make_key(field_key, exclude_last_string=True)

                    field_value.widget.attrs['class'] += " embeddedField"

                    # Setting the embedded key correctly allows to visually nest the
                    # embedded documents on the front end.
                    if base_key == parent_key:
                        field_value.widget.attrs['class'] += ' {0}'.format(base_key)
                    else:
                        field_value.widget.attrs['class'] += ' {0} {1}'.format(base_key, parent_key)

                    if embedded_key_class is not None:
                        field_value.widget.attrs['class'] += ' {0}'.format(embedded_key_class)

                default_value = self.get_field_value(form_key)

                # Style embedded documents
                if isinstance(default_value, list) and len(default_value) > 0:
                    key_index = int(form_key.split("_")[-1])
                    new_base_key = make_key(form_key, exclude_last_string=True)

                    for list_value in default_value:
                        # Note, this is copied every time so each widget gets a different class
                        list_widget = deepcopy(field_value.widget)
                        new_key = make_key(new_base_key, six.text_type(key_index))
                        list_widget.attrs['class'] += " {0}".format(make_key(base_key, key_index))
                        self.set_form_field(list_widget, field_value.document_field, new_key, list_value)
                        key_index += 1
                else:
                    self.set_form_field(field_value.widget, field_value.document_field,
                                        form_key, default_value)

            elif isinstance(field_value, dict):
                self.set_form_fields(field_value, form_key, field_value.get("_field_type", None))