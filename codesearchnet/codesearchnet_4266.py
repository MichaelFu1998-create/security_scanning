def set_pkg_licenses_concluded(self, doc, licenses):
        """Sets the package's concluded licenses.
        licenses - License info.
        Raises CardinalityError if already defined.
        Raises OrderError if no package previously defined.
        Raises SPDXValueError if data malformed.
        """
        self.assert_package_exists()
        if not self.package_conc_lics_set:
            self.package_conc_lics_set = True
            if validations.validate_lics_conc(licenses):
                doc.package.conc_lics = licenses
                return True
            else:
                raise SPDXValueError('Package::ConcludedLicenses')
        else:
            raise CardinalityError('Package::ConcludedLicenses')