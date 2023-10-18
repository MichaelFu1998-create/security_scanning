def set_file_license_comment(self, doc, text):
        """
        Raises OrderError if no package or file defined.
        Raises SPDXValueError if text is not free form text.
        Raises CardinalityError if more than one per file.
        """
        if self.has_package(doc) and self.has_file(doc):
            if not self.file_license_comment_set:
                self.file_license_comment_set = True
                if validations.validate_file_lics_comment(text):
                    self.file(doc).license_comment = str_from_text(text)
                else:
                    raise SPDXValueError('File::LicenseComment')
            else:
                raise CardinalityError('File::LicenseComment')
        else:
            raise OrderError('File::LicenseComment')