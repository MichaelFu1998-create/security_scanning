def parse_only_extr_license(self, extr_lic):
        """
        Return an ExtractedLicense object to represent a license object.
        But does not add it to the SPDXDocument model.
        Return None if failed.
        """
        # Grab all possible values
        ident = self.get_extr_license_ident(extr_lic)
        text = self.get_extr_license_text(extr_lic)
        comment = self.get_extr_lics_comment(extr_lic)
        xrefs = self.get_extr_lics_xref(extr_lic)
        name = self.get_extr_lic_name(extr_lic)

        if not ident:
            # Must have identifier
            return

        # Set fields
        # FIXME: the constructor of the license should alwas accept a name
        lic = document.ExtractedLicense(ident)
        if text is not None:
            lic.text = text
        if name is not None:
            lic.full_name = name
        if comment is not None:
            lic.comment = comment
        lic.cross_ref = map(lambda x: six.text_type(x), xrefs)
        return lic