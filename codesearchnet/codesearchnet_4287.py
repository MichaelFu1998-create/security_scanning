def set_lic_id(self, doc, lic_id):
        """Adds a new extracted license to the document.
        Raises SPDXValueError if data format is incorrect.
        """
        # FIXME: this state does not make sense
        self.reset_extr_lics()
        if validations.validate_extracted_lic_id(lic_id):
            doc.add_extr_lic(document.ExtractedLicense(lic_id))
            return True
        else:
            raise SPDXValueError('ExtractedLicense::id')