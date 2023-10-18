def create_license_node(self, lic):
        """
        Return a node representing a license.
        Could be a single license (extracted or part of license list.) or
        a conjunction/disjunction of licenses.
        """
        if isinstance(lic, document.LicenseConjunction):
            return self.create_conjunction_node(lic)
        elif isinstance(lic, document.LicenseDisjunction):
            return self.create_disjunction_node(lic)
        else:
            return self.create_license_helper(lic)