def get_form_field_dict(self, model_dict):
        """
        Takes a model dictionary representation and creates a dictionary
        keyed by form field.  Each value is a  keyed 4 tuple of:
        (widget, mode_field_instance, model_field_type, field_key)
        """
        return_dict = OrderedDict()
        # Workaround: mongoengine doesn't preserve form fields ordering from metaclass __new__
        if hasattr(self.model, 'Meta') and hasattr(self.model.Meta, 'form_fields_ordering'):
            field_order_list = tuple(form_field for form_field
                                     in self.model.Meta.form_fields_ordering
                                     if form_field in model_dict.iterkeys())
            order_dict = OrderedDict.fromkeys(field_order_list)
            return_dict = order_dict

        for field_key, field_dict in sorted(model_dict.items()):
            if not field_key.startswith("_"):
                widget = field_dict.get('_widget', None)
                if widget is None:
                    return_dict[field_key] = self.get_form_field_dict(field_dict)
                    return_dict[field_key].update({'_field_type': field_dict.get('_field_type', None)})
                else:
                    return_dict[field_key] = FieldTuple(widget,
                                             field_dict.get('_document_field', None),
                                             field_dict.get('_field_type', None),
                                             field_dict.get('_key', None))
        return return_dict