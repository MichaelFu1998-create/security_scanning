def validate_mandatory_str_fields(self, messages):
        """Fields marked as Mandatory and of type string in class
        docstring must be of a type that provides __str__ method.
        """
        FIELDS = ['name', 'download_location', 'verif_code', 'cr_text']
        messages = self.validate_str_fields(FIELDS, False, messages)

        return messages