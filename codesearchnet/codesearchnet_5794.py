def _refresh(self, http):
        """Refreshes the access token.

        Args:
            http: unused HTTP object
        """
        self.devshell_response = _SendRecv()
        self.access_token = self.devshell_response.access_token
        expires_in = self.devshell_response.expires_in
        if expires_in is not None:
            delta = datetime.timedelta(seconds=expires_in)
            self.token_expiry = client._UTCNOW() + delta
        else:
            self.token_expiry = None