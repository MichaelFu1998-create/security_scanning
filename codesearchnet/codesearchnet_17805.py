def get_unique_token(self):
        """
        Get a unique token for usage in differentiating test runs that need to
        run in parallel.
        """
        if self._unique_token is None:
            self._unique_token = self._random_token()

        return self._unique_token