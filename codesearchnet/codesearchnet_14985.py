def revoke_token(self, token):
        """
        Implementation of :meth:`twitcher.api.ITokenManager.revoke_token`.
        """
        try:
            self.store.delete_token(token)
        except Exception:
            LOGGER.exception('Failed to remove token.')
            return False
        else:
            return True