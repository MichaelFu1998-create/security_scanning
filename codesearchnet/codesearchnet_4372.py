def set_pkg_cr_text(self, doc, text):
        """Sets the package's license comment.
        Raises OrderError if no package previously defined.
        Raises CardinalityError if already set.
        """
        self.assert_package_exists()
        if not self.package_cr_text_set:
            self.package_cr_text_set = True
            doc.package.cr_text = text
        else:
            raise CardinalityError('Package::CopyrightText')