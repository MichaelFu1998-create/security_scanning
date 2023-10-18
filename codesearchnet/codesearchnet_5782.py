def locked_put(self, credentials):
        """Write a Credentials to the datastore.

        Args:
            credentials: Credentials, the credentials to store.
        """
        entity = self._model.get_or_insert(self._key_name)
        setattr(entity, self._property_name, credentials)
        entity.put()
        if self._cache:
            self._cache.set(self._key_name, credentials.to_json())