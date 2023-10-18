def _generate_assertion(self):
        """Generate the assertion that will be used in the request."""
        now = int(time.time())
        payload = {
            'aud': self.token_uri,
            'scope': self._scopes,
            'iat': now,
            'exp': now + self.MAX_TOKEN_LIFETIME_SECS,
            'iss': self._service_account_email,
        }
        payload.update(self._kwargs)
        return crypt.make_signed_jwt(self._signer, payload,
                                     key_id=self._private_key_id)