def locked_get(self):
        """Retrieve the credentials from the dictionary, if they exist.

        Returns: A :class:`oauth2client.client.OAuth2Credentials` instance.
        """
        serialized = self._dictionary.get(self._key)

        if serialized is None:
            return None

        credentials = client.OAuth2Credentials.from_json(serialized)
        credentials.set_store(self)

        return credentials