def handle_lics(self, lics):
        """
        Return a License from a `lics` license resource.
        """
        # Handle extracted licensing info type.
        if (lics, RDF.type, self.spdx_namespace['ExtractedLicensingInfo']) in self.graph:
            return self.parse_only_extr_license(lics)

        # Assume resource, hence the path separator
        ident_start = lics.rfind('/') + 1
        if ident_start == 0:
            # special values such as spdx:noassertion
            special = self.to_special_value(lics)
            if special == lics:
                if self.LICS_REF_REGEX.match(lics):
                    # Is a license ref i.e LicenseRef-1
                    return document.License.from_identifier(lics)
                else:
                    # Not a known license form
                    raise SPDXValueError('License')
            else:
                # is a special value
                return special
        else:
            # license url
            return document.License.from_identifier(lics[ident_start:])