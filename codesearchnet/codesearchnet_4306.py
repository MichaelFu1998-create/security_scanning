def license_or_special(self, lic):
        """
        Check for special values spdx:none and spdx:noassertion.
        Return the term for the special value or the result of passing
        license to create_license_node.
        """
        if isinstance(lic, utils.NoAssert):
            return self.spdx_namespace.noassertion
        elif isinstance(lic, utils.SPDXNone):
            return self.spdx_namespace.none
        else:
            return self.create_license_node(lic)