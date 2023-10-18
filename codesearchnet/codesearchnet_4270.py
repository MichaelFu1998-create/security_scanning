def set_pkg_cr_text(self, doc, text):
        """Sets the package's copyright text.
        Raises OrderError if no package previously defined.
        Raises CardinalityError if already set.
        Raises value error if text is not one of [None, NOASSERT, TEXT].
        """
        self.assert_package_exists()
        if not self.package_cr_text_set:
            self.package_cr_text_set = True
            if validations.validate_pkg_cr_text(text):
                if isinstance(text, string_types):
                    doc.package.cr_text = str_from_text(text)
                else:
                    doc.package.cr_text = text  # None or NoAssert
            else:
                raise SPDXValueError('Package::CopyrightText')
        else:
            raise CardinalityError('Package::CopyrightText')