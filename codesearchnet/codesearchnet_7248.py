def set(self, refresh_token):
        """Cache a refresh token, ignoring any failure.

        Args:
            refresh_token (str): Refresh token to cache.
        """
        logger.info('Saving refresh_token to %s', repr(self._filename))
        try:
            with open(self._filename, 'w') as f:
                f.write(refresh_token)
        except IOError as e:
            logger.warning('Failed to save refresh_token: %s', e)