def set_property_value(self, name, value, dry_run=False):
        """Set or remove property value.

        See DAVResource.set_property_value()
        """
        if value is None:
            # We can never remove properties
            raise DAVError(HTTP_FORBIDDEN)
        if name == "{virtres:}tags":
            # value is of type etree.Element
            self.data["tags"] = value.text.split(",")
        elif name == "{virtres:}description":
            # value is of type etree.Element
            self.data["description"] = value.text
        elif name in VirtualResource._supportedProps:
            # Supported property, but read-only
            raise DAVError(
                HTTP_FORBIDDEN, err_condition=PRECONDITION_CODE_ProtectedProperty
            )
        else:
            # Unsupported property
            raise DAVError(HTTP_FORBIDDEN)
        # Write OK
        return