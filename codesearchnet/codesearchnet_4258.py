def set_pkg_file_name(self, doc, name):
        """Sets the package file name, if not already set.
        name - Any string.
        Raises CardinalityError if already has a file_name.
        Raises OrderError if no pacakge previously defined.
        """
        self.assert_package_exists()
        if not self.package_file_name_set:
            self.package_file_name_set = True
            doc.package.file_name = name
            return True
        else:
            raise CardinalityError('Package::FileName')