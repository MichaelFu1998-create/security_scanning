def _load_config(self, client_secrets_file, client_id, client_secret):
        """Loads oauth2 configuration in order of priority.

        Priority:
            1. Config passed to the constructor or init_app.
            2. Config passed via the GOOGLE_OAUTH2_CLIENT_SECRETS_FILE app
               config.
            3. Config passed via the GOOGLE_OAUTH2_CLIENT_ID and
               GOOGLE_OAUTH2_CLIENT_SECRET app config.

        Raises:
            ValueError if no config could be found.
        """
        if client_id and client_secret:
            self.client_id, self.client_secret = client_id, client_secret
            return

        if client_secrets_file:
            self._load_client_secrets(client_secrets_file)
            return

        if 'GOOGLE_OAUTH2_CLIENT_SECRETS_FILE' in self.app.config:
            self._load_client_secrets(
                self.app.config['GOOGLE_OAUTH2_CLIENT_SECRETS_FILE'])
            return

        try:
            self.client_id, self.client_secret = (
                self.app.config['GOOGLE_OAUTH2_CLIENT_ID'],
                self.app.config['GOOGLE_OAUTH2_CLIENT_SECRET'])
        except KeyError:
            raise ValueError(
                'OAuth2 configuration could not be found. Either specify the '
                'client_secrets_file or client_id and client_secret or set '
                'the app configuration variables '
                'GOOGLE_OAUTH2_CLIENT_SECRETS_FILE or '
                'GOOGLE_OAUTH2_CLIENT_ID and GOOGLE_OAUTH2_CLIENT_SECRET.')