def set_pkg_license_from_file(self, doc, lic):
        """Adds a license from a file to the package.
        Raises SPDXValueError if data malformed.
        Raises OrderError if no package previously defined.
        """
        self.assert_package_exists()
        if validations.validate_lics_from_file(lic):
            doc.package.licenses_from_files.append(lic)
            return True
        else:
            raise SPDXValueError('Package::LicensesFromFile')