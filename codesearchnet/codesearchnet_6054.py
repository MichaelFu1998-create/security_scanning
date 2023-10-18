def set_property_value(self, name, value, dry_run=False):
        """Set or remove property value.

        See DAVResource.set_property_value()
        """
        raise DAVError(
            HTTP_FORBIDDEN, err_condition=PRECONDITION_CODE_ProtectedProperty
        )