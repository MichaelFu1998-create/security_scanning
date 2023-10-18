def _from_base_type(self, value):
        """Converts our stored JSON string back to the desired type.

        Args:
            value: A value from the datastore to be converted to the
                   desired type.

        Returns:
            A deserialized Credentials (or subclass) object, else None if
            the value can't be parsed.
        """
        if not value:
            return None
        try:
            # Uses the from_json method of the implied class of value
            credentials = client.Credentials.new_from_json(value)
        except ValueError:
            credentials = None
        return credentials