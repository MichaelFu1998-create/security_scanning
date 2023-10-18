def create_license_helper(self, lic):
        """
        Handle single(no conjunction/disjunction) licenses.
        Return the created node.
        """
        if isinstance(lic, document.ExtractedLicense):
            return self.create_extracted_license(lic)
        if lic.identifier.rstrip('+') in config.LICENSE_MAP:
            return URIRef(lic.url)
        else:
            matches = [l for l in self.document.extracted_licenses if l.identifier == lic.identifier]
            if len(matches) != 0:
                return self.create_extracted_license(matches[0])
            else:
                raise InvalidDocumentError('Missing extracted license: {0}'.format(lic.identifier))