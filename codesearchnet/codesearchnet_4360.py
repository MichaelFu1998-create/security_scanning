def validate_optional_str_fields(self, messages):
        """Fields marked as optional and of type string in class
        docstring must be of a type that provides __str__ method.
        """
        FIELDS = [
            'file_name',
            'version',
            'homepage',
            'source_info',
            'summary',
            'description'
        ]
        messages = self.validate_str_fields(FIELDS, True, messages)

        return messages