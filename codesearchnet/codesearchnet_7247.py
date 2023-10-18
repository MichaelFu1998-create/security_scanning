def get(self):
        """Get cached refresh token.

        Returns:
            Cached refresh token, or ``None`` on failure.
        """
        logger.info(
            'Loading refresh_token from %s', repr(self._filename)
        )
        try:
            with open(self._filename) as f:
                return f.read()
        except IOError as e:
            logger.info('Failed to load refresh_token: %s', e)