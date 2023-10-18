def set_pkg_summary(self, doc, text):
        """Set's the package summary.
        Raises SPDXValueError if text is not free form text.
        Raises CardinalityError if summary already set.
        Raises OrderError if no package previously defined.
        """
        self.assert_package_exists()
        if not self.package_summary_set:
            self.package_summary_set = True
            if validations.validate_pkg_summary(text):
                doc.package.summary = str_from_text(text)
            else:
                raise SPDXValueError('Package::Summary')
        else:
            raise CardinalityError('Package::Summary')