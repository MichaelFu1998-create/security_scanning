def set_pkg_desc(self, doc, text):
        """Set's the package's description.
        Raises CardinalityError if description already set.
        Raises OrderError if no package previously defined.
        """
        self.assert_package_exists()
        if not self.package_desc_set:
            self.package_desc_set = True
            doc.package.description = text
        else:
            raise CardinalityError('Package::Description')