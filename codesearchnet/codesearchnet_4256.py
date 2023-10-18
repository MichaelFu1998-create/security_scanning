def create_package(self, doc, name):
        """Creates a package for the SPDX Document.
        name - any string.
        Raises CardinalityError if package already defined.
        """
        if not self.package_set:
            self.package_set = True
            doc.package = package.Package(name=name)
            return True
        else:
            raise CardinalityError('Package::Name')