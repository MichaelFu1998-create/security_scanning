def set_lic_name(self, doc, name):
        """Sets license name.
        Raises SPDXValueError if name is not str or utils.NoAssert
        Raises OrderError if no license id defined.
        """
        if self.has_extr_lic(doc):
            if not self.extr_lic_name_set:
                self.extr_lic_name_set = True
                if validations.validate_extr_lic_name(name):
                    self.extr_lic(doc).full_name = name
                    return True
                else:
                    raise SPDXValueError('ExtractedLicense::Name')
            else:
                raise CardinalityError('ExtractedLicense::Name')
        else:
            raise OrderError('ExtractedLicense::Name')