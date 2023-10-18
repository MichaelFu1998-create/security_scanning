def authorized(self):
        """Boolean that indicates whether this session has an OAuth token
        or not. If `self.authorized` is True, you can reasonably expect
        OAuth-protected requests to the resource to succeed. If
        `self.authorized` is False, you need the user to go through the OAuth
        authentication dance before OAuth-protected requests to the resource
        will succeed.
        """
        if self._client.client.signature_method == SIGNATURE_RSA:
            # RSA only uses resource_owner_key
            return bool(self._client.client.resource_owner_key)
        else:
            # other methods of authentication use all three pieces
            return (
                bool(self._client.client.client_secret)
                and bool(self._client.client.resource_owner_key)
                and bool(self._client.client.resource_owner_secret)
            )