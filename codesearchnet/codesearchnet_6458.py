def find_characteristic(self, uuid):
        """Return the first child characteristic found that has the specified
        UUID.  Will return None if no characteristic that matches is found.
        """
        for char in self.list_characteristics():
            if char.uuid == uuid:
                return char
        return None