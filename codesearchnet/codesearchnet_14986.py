def revoke_all_tokens(self):
        """
        Implementation of :meth:`twitcher.api.ITokenManager.revoke_all_tokens`.
        """
        try:
            self.store.clear_tokens()
        except Exception:
            LOGGER.exception('Failed to remove tokens.')
            return False
        else:
            return True