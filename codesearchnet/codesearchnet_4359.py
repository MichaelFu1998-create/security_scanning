def validate(self, messages):
        """
        Validate the package fields.
        Append user friendly error messages to the `messages` list.
        """
        messages = self.validate_checksum(messages)
        messages = self.validate_optional_str_fields(messages)
        messages = self.validate_mandatory_str_fields(messages)
        messages = self.validate_files(messages)
        messages = self.validate_mandatory_fields(messages)
        messages = self.validate_optional_fields(messages)

        return messages