def set_pkg_license_comment(self, doc, text):
        """Sets the package's license comment.
        Raises OrderError if no package previously defined.
        Raises CardinalityError if already set.
        """
        self.assert_package_exists()
        if not self.package_license_comment_set:
            self.package_license_comment_set = True
            doc.package.license_comment = text
            return True
        else:
            raise CardinalityError('Package::LicenseComment')