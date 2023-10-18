def handle_extracted_license(self, extr_lic):
        """
        Build and return an ExtractedLicense or None.
        Note that this function adds the license to the document.
        """
        lic = self.parse_only_extr_license(extr_lic)
        if lic is not None:
            self.doc.add_extr_lic(lic)
        return lic