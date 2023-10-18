def set_file_license_comment(self, doc, text):
        """
        Raises OrderError if no package or file defined.
        Raises CardinalityError if more than one per file.
        """
        if self.has_package(doc) and self.has_file(doc):
            if not self.file_license_comment_set:
                self.file_license_comment_set = True
                self.file(doc).license_comment = text
                return True
            else:
                raise CardinalityError('File::LicenseComment')
        else:
            raise OrderError('File::LicenseComment')