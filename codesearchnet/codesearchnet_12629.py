def set_form_field(self, widget, model_field, field_key, default_value):
        """
        Parmams:
            widget -- the widget to use for displyaing the model_field
            model_field -- the field on the model to create a form field with
            field_key -- the name for the field on the form
            default_value -- the value to give for the field
                             Default: None
        """
        # Empty lists cause issues on form validation
        if default_value == []:
            default_value = None

        if widget and isinstance(widget, forms.widgets.Select):
            self.form.fields[field_key] = forms.ChoiceField(label=model_field.name,
                                                            required=model_field.required,
                                                            widget=widget)
        else:
            field_class = get_form_field_class(model_field)
            self.form.fields[field_key] = field_class(label=model_field.name,
                                                      required=model_field.required,
                                                      widget=widget)

        if default_value is not None:
            if isinstance(default_value, Document):
                # Probably a reference field, therefore, add id
                self.form.fields[field_key].initial = getattr(default_value, 'id', None)
            else:
                self.form.fields[field_key].initial = default_value
        else:
            self.form.fields[field_key].initial = getattr(model_field, 'default', None)

        if isinstance(model_field, ReferenceField):
            self.form.fields[field_key].choices = [(six.text_type(x.id), get_document_unicode(x))
                                                    for x in model_field.document_type.objects.all()]
            # Adding in blank choice so a reference field can be deleted by selecting blank
            self.form.fields[field_key].choices.insert(0, ("", ""))

        elif model_field.choices:
            self.form.fields[field_key].choices = model_field.choices

        for key, form_attr in CHECK_ATTRS.items():
            if hasattr(model_field, key):
                value = getattr(model_field, key)
                setattr(self.form.fields[field_key], key, value)