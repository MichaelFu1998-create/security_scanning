def set_pkg_home(self, doc, location):
        """Sets the package homepage location if not already set.
        location - A string or None or NoAssert.
        Raises CardinalityError if already defined.
        Raises OrderError if no package previously defined.
        Raises SPDXValueError if location has incorrect value.
        """
        self.assert_package_exists()
        if not self.package_home_set:
            self.package_home_set = True
            if validations.validate_pkg_homepage(location):
                doc.package.homepage = location
                return True
            else:
                raise SPDXValueError('Package::HomePage')
        else:
            raise CardinalityError('Package::HomePage')