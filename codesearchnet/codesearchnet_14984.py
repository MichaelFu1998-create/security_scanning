def generate_token(self, valid_in_hours=1, data=None):
        """
        Implementation of :meth:`twitcher.api.ITokenManager.generate_token`.
        """
        data = data or {}
        access_token = self.tokengenerator.create_access_token(
            valid_in_hours=valid_in_hours,
            data=data,
        )
        self.store.save_token(access_token)
        return access_token.params