def set_pkg_excl_file(self, doc, filename):
        """Sets the package's verification code excluded file.
        Raises OrderError if no package previously defined.
        """
        self.assert_package_exists()
        doc.package.add_exc_file(filename)