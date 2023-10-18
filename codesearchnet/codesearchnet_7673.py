def get_credential(self, service, username):
        """Gets the username and password for the service.
        Returns a Credential instance.

        The *username* argument is optional and may be omitted by
        the caller or ignored by the backend. Callers must use the
        returned username.
        """
        # The default implementation requires a username here.
        if username is not None:
            password = self.get_password(service, username)
            if password is not None:
                return credentials.SimpleCredential(
                    username,
                    password,
                )
        return None