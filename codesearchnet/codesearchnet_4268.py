def set_pkg_license_declared(self, doc, lic):
        """Sets the package's declared license.
        Raises SPDXValueError if data malformed.
        Raises OrderError if no package previously defined.
        Raises CardinalityError if already set.
        """
        self.assert_package_exists()
        if not self.package_license_declared_set:
            self.package_license_declared_set = True
            if validations.validate_lics_conc(lic):
                doc.package.license_declared = lic
                return True
            else:
                raise SPDXValueError('Package::LicenseDeclared')
        else:
            raise CardinalityError('Package::LicenseDeclared')