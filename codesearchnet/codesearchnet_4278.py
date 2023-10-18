def set_concluded_license(self, doc, lic):
        """
        Raises OrderError if no package or file defined.
        Raises CardinalityError if already set.
        Raises SPDXValueError if malformed.
        """
        if self.has_package(doc) and self.has_file(doc):
            if not self.file_conc_lics_set:
                self.file_conc_lics_set = True
                if validations.validate_lics_conc(lic):
                    self.file(doc).conc_lics = lic
                    return True
                else:
                    raise SPDXValueError('File::ConcludedLicense')
            else:
                raise CardinalityError('File::ConcludedLicense')
        else:
            raise OrderError('File::ConcludedLicense')