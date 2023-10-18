def validate(self, messages):
        """
        Validate all fields of the document and update the
        messages list with user friendly error messages for display.
        """
        messages = self.validate_version(messages)
        messages = self.validate_data_lics(messages)
        messages = self.validate_name(messages)
        messages = self.validate_spdx_id(messages)
        messages = self.validate_namespace(messages)
        messages = self.validate_ext_document_references(messages)
        messages = self.validate_creation_info(messages)
        messages = self.validate_package(messages)
        messages = self.validate_extracted_licenses(messages)
        messages = self.validate_reviews(messages)

        return messages