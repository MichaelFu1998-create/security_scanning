def find_descriptor(self, uuid):
        """Return the first child descriptor found that has the specified
        UUID.  Will return None if no descriptor that matches is found.
        """
        for desc in self.list_descriptors():
            if desc.uuid == uuid:
                return desc
        return None