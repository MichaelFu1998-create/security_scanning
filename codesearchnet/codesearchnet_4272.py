def set_pkg_desc(self, doc, text):
        """Set's the package's description.
        Raises SPDXValueError if text is not free form text.
        Raises CardinalityError if description already set.
        Raises OrderError if no package previously defined.
        """
        self.assert_package_exists()
        if not self.package_desc_set:
            self.package_desc_set = True
            if validations.validate_pkg_desc(text):
                doc.package.description = str_from_text(text)
            else:
                raise SPDXValueError('Package::Description')
        else:
            raise CardinalityError('Package::Description')