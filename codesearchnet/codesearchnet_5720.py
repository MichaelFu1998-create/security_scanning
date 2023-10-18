def put(self, credentials):
        """Write a credential.

        The Storage lock must be held when this is called.

        Args:
            credentials: Credentials, the credentials to store.
        """
        self.acquire_lock()
        try:
            self.locked_put(credentials)
        finally:
            self.release_lock()