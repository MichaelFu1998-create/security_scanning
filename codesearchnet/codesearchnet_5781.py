def locked_get(self):
        """Retrieve Credential from datastore.

        Returns:
            oauth2client.Credentials
        """
        credentials = None
        if self._cache:
            json = self._cache.get(self._key_name)
            if json:
                credentials = client.Credentials.new_from_json(json)
        if credentials is None:
            entity = self._get_entity()
            if entity is not None:
                credentials = getattr(entity, self._property_name)
                if self._cache:
                    self._cache.set(self._key_name, credentials.to_json())

        if credentials and hasattr(credentials, 'set_store'):
            credentials.set_store(self)
        return credentials