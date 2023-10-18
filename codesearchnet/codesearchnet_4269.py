def set_pkg_license_comment(self, doc, text):
        """Sets the package's license comment.
        Raises OrderError if no package previously defined.
        Raises CardinalityError if already set.
        Raises SPDXValueError if text is not free form text.
        """
        self.assert_package_exists()
        if not self.package_license_comment_set:
            self.package_license_comment_set = True
            if validations.validate_pkg_lics_comment(text):
                doc.package.license_comment = str_from_text(text)
                return True
            else:
                raise SPDXValueError('Package::LicenseComment')
        else:
            raise CardinalityError('Package::LicenseComment')