def set_pkg_summary(self, doc, text):
        """Set's the package summary.
        Raises CardinalityError if summary already set.
        Raises OrderError if no package previously defined.
        """
        self.assert_package_exists()
        if not self.package_summary_set:
            self.package_summary_set = True
            doc.package.summary = text
        else:
            raise CardinalityError('Package::Summary')