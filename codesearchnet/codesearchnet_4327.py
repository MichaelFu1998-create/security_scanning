def get_extr_license_ident(self, extr_lic):
        """
        Return an a license identifier from an ExtractedLicense or None.
        """
        identifier_tripples = list(self.graph.triples((extr_lic, self.spdx_namespace['licenseId'], None)))

        if not identifier_tripples:
            self.error = True
            msg = 'Extracted license must have licenseId property.'
            self.logger.log(msg)
            return

        if len(identifier_tripples) > 1:
            self.more_than_one_error('extracted license identifier_tripples')
            return

        identifier_tripple = identifier_tripples[0]
        _s, _p, identifier = identifier_tripple
        return identifier