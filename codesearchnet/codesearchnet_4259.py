def set_pkg_supplier(self, doc, entity):
        """Sets the package supplier, if not already set.
        entity - Organization, Person or NoAssert.
        Raises CardinalityError if already has a supplier.
        Raises OrderError if no package previously defined.
        """
        self.assert_package_exists()
        if not self.package_supplier_set:
            self.package_supplier_set = True
            if validations.validate_pkg_supplier(entity):
                doc.package.supplier = entity
                return True
            else:
                raise SPDXValueError('Package::Supplier')
        else:
            raise CardinalityError('Package::Supplier')