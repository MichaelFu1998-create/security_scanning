def _handle_license_list(self, lics_set, cls=None):
        """
        Return a license representing a `cls` object (LicenseConjunction
        or LicenseDisjunction) from a list of license resources or None.
        """
        licenses = []
        for _, _, lics_member in self.graph.triples(
            (lics_set, self.spdx_namespace['member'], None)):
            try:
                if (lics_member, RDF.type, self.spdx_namespace['ExtractedLicensingInfo']) in self.graph:
                    lics = self.handle_extracted_license(lics_member)
                    if lics is not None:
                        licenses.append(lics)
                else:
                    licenses.append(self.handle_lics(lics_member))
            except CardinalityError:
                self.value_error('LICS_LIST_MEMBER', lics_member)
                break
        if len(licenses) > 1:
            return reduce(lambda a, b: cls(a, b), licenses)
        else:
            self.value_error('PKG_CONC_LIST', '')
            return