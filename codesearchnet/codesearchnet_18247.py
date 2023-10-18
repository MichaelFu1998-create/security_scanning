def _to_primary_key(self, value):
        """
        Return primary key; if value is StoredObject, verify
        that it is loaded.

        """
        if value is None:
            return None
        if isinstance(value, self.base_class):
            if not value._is_loaded:
                raise exceptions.DatabaseError('Record must be loaded.')
            return value._primary_key

        return self.base_class._to_primary_key(value)