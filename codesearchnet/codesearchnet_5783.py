def locked_delete(self):
        """Delete Credential from datastore."""

        if self._cache:
            self._cache.delete(self._key_name)

        self._delete_entity()