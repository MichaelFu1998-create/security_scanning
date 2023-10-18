def validate_str_fields(self, fields, optional, messages):
        """Helper for validate_mandatory_str_field and
        validate_optional_str_fields"""
        for field_str in fields:
            field = getattr(self, field_str)
            if field is not None:
                # FIXME: this does not make sense???
                attr = getattr(field, '__str__', None)
                if not callable(attr):
                    messages = messages + [
                        '{0} must provide __str__ method.'.format(field)
                    ]
                    # Continue checking.
            elif not optional:
                messages = messages + [
                    'Package {0} can not be None.'.format(field_str)
                ]

        return messages