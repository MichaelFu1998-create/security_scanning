def locked_put(self, credentials):
        """Save the credentials to the dictionary.

        Args:
            credentials: A :class:`oauth2client.client.OAuth2Credentials`
                         instance.
        """
        serialized = credentials.to_json()
        self._dictionary[self._key] = serialized