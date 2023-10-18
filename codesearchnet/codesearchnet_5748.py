def locked_get(self):
        """Retrieves the current credentials from the store.

        Returns:
            An instance of :class:`oauth2client.client.Credentials` or `None`.
        """
        credential = self._backend.locked_get(self._key)

        if credential is not None:
            credential.set_store(self)

        return credential