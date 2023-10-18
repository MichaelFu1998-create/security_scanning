def set_file_license_in_file(self, doc, lic):
        """
        Raises OrderError if no package or file defined.
        Raises SPDXValueError if malformed value.
        """
        if self.has_package(doc) and self.has_file(doc):
            if validations.validate_file_lics_in_file(lic):
                self.file(doc).add_lics(lic)
                return True
            else:
                raise SPDXValueError('File::LicenseInFile')
        else:
            raise OrderError('File::LicenseInFile')