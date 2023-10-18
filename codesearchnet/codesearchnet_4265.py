def set_pkg_source_info(self, doc, text):
        """Sets the package's source information, if not already set.
        text - Free form text.
        Raises CardinalityError if already defined.
        Raises OrderError if no package previously defined.
        SPDXValueError if text is not free form text.
        """
        self.assert_package_exists()
        if not self.package_source_info_set:
            self.package_source_info_set = True
            if validations.validate_pkg_src_info(text):
                doc.package.source_info = str_from_text(text)
                return True
            else:
                raise SPDXValueError('Pacckage::SourceInfo')
        else:
            raise CardinalityError('Package::SourceInfo')