def set_pkg_vers(self, doc, version):
        """Sets package version, if not already set.
        version - Any string.
        Raises CardinalityError if already has a version.
        Raises OrderError if no package previously defined.
        """
        self.assert_package_exists()
        if not self.package_vers_set:
            self.package_vers_set = True
            doc.package.version = version
            return True
        else:
            raise CardinalityError('Package::Version')