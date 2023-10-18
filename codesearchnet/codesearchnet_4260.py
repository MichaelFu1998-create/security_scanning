def set_pkg_originator(self, doc, entity):
        """Sets the package originator, if not already set.
        entity - Organization, Person or NoAssert.
        Raises CardinalityError if already has an originator.
        Raises OrderError if no package previously defined.
        """
        self.assert_package_exists()
        if not self.package_originator_set:
            self.package_originator_set = True
            if validations.validate_pkg_originator(entity):
                doc.package.originator = entity
                return True
            else:
                raise SPDXValueError('Package::Originator')
        else:
            raise CardinalityError('Package::Originator')