def _create_session(self, scope):
        """
        Instantiate a new session object for use in connecting with Degreed
        """
        now = datetime.datetime.utcnow()
        if self.session is None or self.expires_at is None or now >= self.expires_at:
            # Create a new session with a valid token
            if self.session:
                self.session.close()
            oauth_access_token, expires_at = self._get_oauth_access_token(
                self.enterprise_configuration.key,
                self.enterprise_configuration.secret,
                self.enterprise_configuration.degreed_user_id,
                self.enterprise_configuration.degreed_user_password,
                scope
            )
            session = requests.Session()
            session.timeout = self.SESSION_TIMEOUT
            session.headers['Authorization'] = 'Bearer {}'.format(oauth_access_token)
            session.headers['content-type'] = 'application/json'
            self.session = session
            self.expires_at = expires_at