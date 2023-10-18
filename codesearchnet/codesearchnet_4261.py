def set_pkg_down_location(self, doc, location):
        """Sets the package download location, if not already set.
        location - A string
        Raises CardinalityError if already defined.
        Raises OrderError if no package previously defined.
        """
        self.assert_package_exists()
        if not self.package_down_location_set:
            self.package_down_location_set = True
            doc.package.download_location = location
            return True
        else:
            raise CardinalityError('Package::DownloadLocation')