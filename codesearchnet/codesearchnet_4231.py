def set_doc_data_lics(self, doc, lics):
        """Sets the document data license.
        Raises value error if malformed value, CardinalityError
        if already defined.
        """
        if not self.doc_data_lics_set:
            self.doc_data_lics_set = True
            if validations.validate_data_lics(lics):
                doc.data_license = document.License.from_identifier(lics)
                return True
            else:
                raise SPDXValueError('Document::DataLicense')
        else:
            raise CardinalityError('Document::DataLicense')